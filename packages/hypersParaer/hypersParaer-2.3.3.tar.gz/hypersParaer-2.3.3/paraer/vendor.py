import collections
import functools
import urllib
import typing

import pandas as pd
from django.conf import settings
from django.db.models import Model, QuerySet
from paraer import Result as BaseResult
from paraer import para_ok_or_400
from django.http import HttpResponse
from rest_framework import exceptions, permissions, status
from rest_framework.compat import coreapi
from rest_framework.exceptions import APIException
from rest_framework.pagination import BasePagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView as _APIView
from rest_framework.viewsets import ViewSet as _ViewSet


class HTTPResult(BaseResult):
    def response(
        self,
        data,
        status: int = 200,
        serialize: bool = True,
        paginate: bool = True,
        filename: str = "",
        header: typing.List[str] = [],
        extractor: typing.Callable = None,
        **kwargs
    ) -> Response:
        """__call__ 生成Response，并且判断是否需要序列化，是否需要分页
        参考
        https://confluence.hypers.com/pages/viewpage.action?pageId=13008984&focusedCommentId=19532896
        Status: 422 Unprocessable Entity
        {
        "message": "字段校验失败",
        "fields": {
            "email": [
                {
                    "code": "invalid",
                    "message": "邮箱格式不合法"
                }
                ]
            }
        }
        
        :param status: 返回的HTTP状态码, defaults to 200
        :type status: int, optional
        :param serialize: 是否需要序列化, defaults to True
        :type serialize: bool, optional
        :param paginate: 是否需要分页, defaults to False
        :type paginate: bool, optional
        :param filename: 生成的csv或excel文件名
        :type filename: str, optional
        :param header: 生成的csv或excel的表头
        :type header: typing.List, optional
        :param extractor: 生成的csv或excel的提取方法，dataset从data中提取
        :type header: typing.Callable , optional
        :return: 返回的HTTP Response
        :rtype: Response
        """
        if status == 422:
            response = dict(
                message="字段校验失败",
                fields={
                    key: [dict(code="invalid", message=value)]
                    for key, value in self.errors
                },
            )
        elif status == 403:
            response = dict(message="该用户不存在或您无权访问")
        elif status == 404:
            response = dict(message="页面不存在或无法访问")
        elif status in [202, 204]:
            response = ""
        else:
            should_serialize = self.serializer and serialize
            if isinstance(data, collections.Iterable) or (
                isinstance(data, dict) and extractor
            ):
                httpResponse = handleContentType(
                    self.request, data, filename, header, extractor
                )
                if httpResponse:
                    return httpResponse
            if isinstance(data, collections.Iterable) and not isinstance(data, dict):
                if should_serialize and (data and isinstance(data[0], Model)):
                    data = self.serializer(data, many=True).data
                if paginate:
                    response = self.paginator.paginate_queryset(data, self.request)
                else:
                    response = data
            elif should_serialize and isinstance(data, Model):
                response = self.serializer(data).data
            else:
                response = data

        return Response(response, status=status)


def handleContentType(
    request: Request,
    data: list,
    filename: str,
    header: typing.List[str],
    extractor: typing.Callable,
) -> HttpResponse:
    if request.META.get("CONTENT_TYPE") == "text/csv" or request.path.endswith(".csv"):
        return handleCsv(request, data, filename, header, extractor)


def handleCsv(
    request: Request,
    data: list,
    filename,
    header: typing.List[str],
    extractor: typing.Callable,
) -> HttpResponse:
    if (
        not isinstance(data, pd.DataFrame) and data and extractor
    ):  # lambda x: x['regionRatio']
        data = extractor(data)
    df = pd.DataFrame(data)
    response = HttpResponse(content_type="text/csv")
    df.to_csv(response, index=False, index_label=header, encoding="utf-8-sig")
    disposition = "attachment; filename=" + urllib.parse.quote_plus(filename)
    response["Content-Disposition"] = disposition
    return response


class Result(BaseResult):
    def __init__(self, data=None, errors=None, serializer=None, paginator=None):
        self.serializer = serializer
        self.data = data
        self._fields = {}
        self._message = None
        self.paginator = paginator
        self._code = 200

    def error(self, key, value, **kwargs):
        self._code = "200002"
        value = [{"code": "200002", "message": value}]
        self._fields[key] = value
        return self

    def perm(self, reason):
        self._message = reason
        return self

    def status(self, code, msg=None):
        """
        设置403等状态码的状态
        """
        self._code = code
        if msg:
            self._message = msg
        return self

    def __call__(self, status=200, serialize=True, **kwargs):
        """
        参考
        https://confluence.hypers.com/pages/viewpage.action?pageId=13008984&focusedCommentId=19532896
        :status: 返回的状态码
        :serialize: bool 是否根绝self.serializer_class 对data做序列化
        :return:
        Status: 422 Unprocessable Entity
        {
        "message": "字段校验失败",
        "fields": {
            "email": [
            {
                "code": "invalid",
                "message": "邮箱格式不合法"
            }
            ]
        }
        }
        """
        data = self.data
        should_serialize = self.serializer and serialize
        response = dict(code=self._code)
        if isinstance(data, collections.Iterable) and not (
            isinstance(data, dict)
        ):  # list 方法返回可迭代对象
            if should_serialize and (data and isinstance(data[0], Model)):
                data = self.serializer(data, many=True).data
            response = self.paginator.paginate_queryset(data, self.paginator.request)
        elif should_serialize and isinstance(data, Model):
            response["result"] = self.serializer(data).data
        else:
            response["result"] = data
        # 参数错误
        if self._fields:
            response["fields"] = self._fields
        if self._message:
            response["message"] = self._message
        return Response(response, **kwargs)

    def redirect(self, path="", status=403, **kwargs):
        data = dict(code="200302")

        if not path and status in [403, 404]:
            path = "/#/error?code={}".format(status)
        data.update(url=path)

        # reason
        reason = kwargs.get("reason", "")
        if isinstance(reason, dict):
            for k, v in reason.items():
                reason = "对{}{}".format(k, v)
        reason and data.update(reason=reason)
        return Response(data, status=200)


def getPageParams(request, keys, pagesizeKey="pagesize"):
    page = str(request.GET.get("page", 1))
    page = int(page.isdigit() and page or 1)
    iTotalRecords = len(keys)
    pagesize = str(request.GET.get(pagesizeKey, iTotalRecords))
    split = pagesize.isdigit()
    pagesize = int(pagesize.isdigit() and pagesize or 10)

    startRecord = (page - 1) * pagesize
    endRecord = (
        iTotalRecords
        if iTotalRecords - startRecord < pagesize
        else startRecord + pagesize
    )

    return startRecord, endRecord, pagesize, iTotalRecords, split


class HTTPPaginator(BasePagination):
    page_query_param = "page"
    page_size_query_param = "pageSize"

    def paginate_queryset(self, keys, request, **kwargs):
        """

        :param keys:
        :param request:
        :param kwargs:
        :return:
        """
        result = dict(page={}, records=[])

        start, end, pagesize, iTotalRecords, split = getPageParams(
            request, keys, self.page_size_query_param
        )
        if not isinstance(keys, list):  # py3兼容 dict_values不是list
            keys = list(keys)

        if split:
            keys = keys[start:end]
        else:
            pagesize = iTotalRecords

        result["page"]["current"] = start
        result["page"]["total"] = iTotalRecords
        result["page"]["size"] = pagesize
        result["records"] = keys
        return result

    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(
                name=self.page_query_param,
                required=False,
                location="query",
                description=u"分页参数：当为空时，获取全量数据",
                type="integer",
            )
        ]
        if self.page_size_query_param is not None:
            fields.append(
                coreapi.Field(
                    name=self.page_size_query_param,
                    required=False,
                    location="query",
                    description=u"分页参数：当为空时，获取全量数据，当传值时，支持[10, 25, 50, 100]分页",
                    type="integer",
                )
            )
        return fields


class PageNumberPager(BasePagination):
    page_query_param = "page"
    page_size_query_param = "pagesize"

    def paginate_queryset(self, keys, request, **kwargs):
        """

        :param keys:
        :param request:
        :param kwargs:
        :return:
        """
        result = {
            "code": "200000",
            "page": {"current": 0, "pagesize": 10, "total": 0},
            "result": {},
        }

        start, end, pagesize, iTotalRecords, split = getPageParams(request, keys)
        if not isinstance(keys, list):  # py3兼容 dict_values不是list
            keys = list(keys)

        if split:
            keys = keys[start:end]
        else:
            pagesize = iTotalRecords

        result["page"]["current"] = start
        result["page"]["total"] = iTotalRecords
        result["page"]["pagesize"] = pagesize
        result["result"]["items"] = keys
        return result

    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(
                name=self.page_query_param,
                required=False,
                location="query",
                description=u"分页参数：当为空时，获取全量数据",
                type="integer",
            )
        ]
        if self.page_size_query_param is not None:
            fields.append(
                coreapi.Field(
                    name=self.page_size_query_param,
                    required=False,
                    location="query",
                    description=u"分页参数：当为空时，获取全量数据，当传值时，支持[10, 25, 50, 100]分页",
                    type="integer",
                )
            )
        return fields


class MixinView(object):
    result_klass = HTTPResult
    serializer_class = None
    pagination_class = HTTPPaginator

    @property
    def result_class(self):
        paginator = self.paginator
        paginator.request = self.request
        return functools.partial(
            self.result_klass,
            serializer=self.serializer_class,
            paginator=paginator,
            request=self.request,
        )

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator


class ViewSet(MixinView, _ViewSet):
    permission_classes = (permissions.IsAuthenticated,)


class APIView(MixinView, _APIView):
    permission_classes = (permissions.IsAuthenticated,)


class UnAuthApiView(MixinView, _APIView):
    authentication_classes = []

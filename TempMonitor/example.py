import urllib3

# data = urllib3.post('http://t-open.tzonedigital.cn/ajax/iHistory.ashx?M=GetTAG04&sn=', json=options)
# print(data)


def prepare_cloud_request(begin_time=None, end_time=None, allow_paging=True, num_results=100, total_count=0, page_index=1):
    return {
        "BeginTime": begin_time,
        "EndTime": end_time,
        "AllowPaging": allow_paging,
        "PageSize": f"{num_results}",
        "TotalCount": total_count,
        "PageIndex": page_index
    }

# dao.core.py

import utils.http


class Endpoint():
    def __init__(self) -> None:
        pass

    def get_data(self, api, url, endpoint, limit, batchSize) -> list:
        offset = 0
        result = []
        records = utils.http.get_http(uri=f'{url}?limit={batchSize}&offset={offset}', API=api)
        if records[endpoint] == [None]:
            return None
        actualCount = records['totalCount']
        if limit in [0, None, False]:
            limit = actualCount
        processed = 0
        print(processed)
        while (actualCount - processed) > 0:
            for record in records[endpoint]:
                if processed >= limit:
                    break
                result.append(record)
                processed += 1
            print(processed)
            if processed >= limit:
                break
            records = utils.http.get_http(uri=f'{url}?limit={batchSize}&offset={processed}', API=api)
#            if records[endpoint] == [None]:
#                break
        print(processed)
        return result

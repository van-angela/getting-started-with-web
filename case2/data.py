import csv

empty_meeting_time = []
meeting_time_with_day = {}
meeting_time_with_time = {}
results = {}

a = [{'key': 'value'}]


def read_file():
    with open("classes.csv", "r") as file:
        rows = csv.DictReader(file)
        for row in rows:
            if not row['Meeting Times']:
                empty_meeting_time.append(row)
                continue
            if ',' in row['Meeting Times']:
                decode_multipart_time(row)
                continue
            put_into_dict(row['Class ID'], row['Meeting Times'].strip())
        # print(meeting_time_with_time)
        # print(meeting_time_with_day)
        # print(empty_meeting_time)
    for key in meeting_time_with_day.keys():
        results[key] = meeting_time_with_day[key]
    for key in meeting_time_with_time.keys():
        if key in results:
            results.get(key).append(meeting_time_with_time[key])
            continue
        results[key] = meeting_time_with_time[key]

    for key in results:
        print(key, results[key])


def decode_multipart_time(row):
    # print(row['Meeting Times'])
    meeting_times = row['Meeting Times'].split(',')
    # print(meeting_times)
    class_id = row['Class ID']
    # print(meeting_times)
    for meeting_time in meeting_times:
        put_into_dict(class_id, meeting_time.strip())


def put_into_dict(class_id, meeting_time):
    if len(meeting_time) < 4:
        print('error message', class_id, meeting_time)
        return
    print(meeting_time)
    # 因为D1D2D4D6-US-A/T:3:45 - 4:45 两种类型都带-，所以先判断带有：的
    # return 代表执行到此处不往下执行了
    if ':' in meeting_time:
        key, value = meeting_time.split(':', 1)
        # 问题数据 -:5:00 - 6:00
        if key == '-':
            print('error message', class_id, meeting_time)
            return
        # 如果还没有key
        if class_id not in meeting_time_with_time:
            list = [{key.strip(): value.strip().replace('--', '')}]
            meeting_time_with_time[class_id] = list
            return
        # 已经存在key
        list = meeting_time_with_time[class_id]
        list.append({key.strip(): value.strip().replace('--', '')})
        return
    if '-' in meeting_time:
        key, value = meeting_time.split('-', 1)
        # 如果还没有key
        if class_id not in meeting_time_with_day:
            # 创建一个新的list 并且只有一个值是dict类型
            list = [{key.strip(): value.strip()}]
            # meeting_time_with_day dict里面新增一个key是class_id，value是list
            meeting_time_with_day[class_id] = list
            return
        # 已经存在key
        list = meeting_time_with_day[class_id]
        # meeting_time_with_day dict里面已经有 key是class_id，value list中增加一个dict
        list.append({key.strip(): value.strip()})
        return


if __name__ == '__main__':
    read_file()

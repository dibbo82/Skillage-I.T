from pyexcel_ods import get_data


part_data = get_data("Wood Stocks.ods",start_row=4,row_limits=1)
print(json.dumps(part_data))








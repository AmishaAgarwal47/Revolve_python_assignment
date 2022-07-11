import argparse
import datetime
import pandas as pd
import numpy as np
import json
import os

def get_params() -> dict:
    parser = argparse.ArgumentParser(description='DataTest')
    parser.add_argument('--customers_location', required=False, default="../input_data/starter/customers.csv")
    parser.add_argument('--products_location', required=False, default="../input_data/starter/products.csv")
    parser.add_argument('--transactions_location', required=False, default="../input_data/starter/transactions/")
    parser.add_argument('--output_location', required=False, default="../output_data/outputs/")
    return vars(parser.parse_args())


def get_dict(en,path) -> dict:
    #creating a dictionary where key is customer/product id
    key=en+'_id'
    df=pd.read_csv(path)
    df.set_index([key],inplace=True)
    dict=df.to_dict()
    return dict


def create_output_json(out_path,data,product_dict,customer_dict):
    #creating final json
    output_json={}
    
    os.makedirs(out_path, exist_ok=True)
    out_path = out_path + "/output.json"
    for cust_id in data.keys():
        output_json['customer_id']=cust_id
        output_json['loyalty_score']=customer_dict['loyalty_score'][cust_id]

        prod_details=[]
        for prod in data[cust_id]:
            temp_dict={}
            temp_dict['product_id']=prod['product_id']
            temp_dict['product_category']=product_dict['product_category'][prod['product_id']]
            prod_details.append(temp_dict)
        output_json['product_details']=prod_details
        output_json['purchase_count'] = len(data[cust_id])
        
       
        with open(out_path, "a") as outfile:
            outfile.write(json.dumps(output_json)+"\n")



def main():
    params = get_params()
    print(params)
    #this date range must remain within the date limits of data generated else will result in error
    start= datetime.date(2018, 12, 1)
    end=datetime.date(2018, 12, 31)
    all_tran_data=append_transactional_data(start,end)
    product_dict= get_dict('product',params['products_location'])
    customer_dict= get_dict('customer',params['customers_location'])
    create_output_json(params['output_location'],all_tran_data,product_dict,customer_dict)


def append_transactional_data(start_date,end_date):
    data={}
    while start_date <= end_date:
        file_name = 'd='+str(start_date) #creating for every day
        path = f"..\\input_data\\starter\\transactions\\{file_name}\\transactions.json"
        
        with open(path) as json_file:
            lines = json_file.readlines()
            for line in lines:
                temp_data=json.loads(line)
                key=temp_data['customer_id']
                if key not in data:
                    data[key]=temp_data['basket']
                else:
                    value=data[key]
                    value.extend(temp_data['basket'])
                    data[key]=value
        start_date=start_date+datetime.timedelta(days=1) #incrementing to each day
    return data
        

if __name__ == "__main__":
    main()

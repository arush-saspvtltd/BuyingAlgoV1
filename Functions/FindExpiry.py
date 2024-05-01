def findExpiry(index , ATMStrike):
    
    file = open("instruments.txt" , 'r').read()
   
    from datetime import datetime

    def closest_expiry_symbol(data_list):
        today = datetime.now().date()
        closest_symbol = None
        min_difference = float("inf")

        for data in data_list:
            values = data.split(",")
            expiry_date_str = values[5]  # Assuming expiry is the 6th value in the array
            expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
            difference = abs((expiry_date - today).days)

            if difference < min_difference:
                min_difference = difference
                closest_symbol = values[2]  # Assuming tradingsymbol is the 3rd value in the array

        return closest_symbol

    # Example usage
    data_list = []
    if index == 'SENSEX':
                FNO_Check = 'BFO-OPT'
    else : FNO_Check ='NFO-OPT'
    for i in file.split("\n"):
        try:
        
            if(len(i.split(','))>5  and i.split(',')[10]==FNO_Check and i.split(',')[3][1:-1]==index and i.split(',')[6]==str(int(ATMStrike))):
                # print(i)
                data_list.append(i)
                # print(i)
            
        except Exception as e :
            print()
            # print(e)


    closest_symbol = closest_expiry_symbol(data_list)
    # print(f"The symbol with the closest expiry date is {closest_symbol}")
    
    def extract_expiry_from_code(index, strike, code):
        # Calculate the position of the strike within the code
       
        start_index = code.find(str(strike))
        strike_position = len(index) + len(str(strike))

        
        # Extract the 3-letter expiry
        expiry = code[len(index)+2:start_index]
        
        
        return expiry

    # Example inputs
    index = index
    strike = ATMStrike
    code = closest_symbol

    expiry = extract_expiry_from_code(index, strike, code)
    return expiry

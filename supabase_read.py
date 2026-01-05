from supabase import create_client
url = "https://cdxnmcpozkfdiqjsthqs.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNkeG5tY3BvemtmZGlxanN0aHFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIzMTk1NzEsImV4cCI6MjA3Nzg5NTU3MX0.wQing-u7lKbYQgXeDvTsTzT5zXVv8Q5Jg1_91PdJxmo"
supabase = create_client(url, key)
def start(indices):
    response = supabase.table("trading_data").select("*").eq("sym", indices).execute()
    data = response.data

    row = data[0]  # first matching row
    id_val = row["id"]
    indices = row["sym"]
    algo = row["algo"]
    lot = row["lot"]
    c_id = row["c_id"]
    c_trade = row["c trade"]
    c_code_1 = row["c code 1"]
    call_op_sym = row["call op sym"]
    c_buy_at = row["c buy at"]
    c_buy_t = row["c buy t"]
    #c_buy_t = datetime.datetime.fromisoformat(c_buy_t)
    c_ltp = row["c ltp"]
    c_r_profit = row["c run pro"]
    c_b_profit = row["c book pro"]
    c_max_hi = row["c max"]
    c_exit_s = row["c exit s"]
    c_exit_at = row["c exit at"]
    c_exit_t = row["c exit time"]
    #c_exit_t = datetime.datetime.fromisoformat(c_exit_t)
    c_mes = row["c message"]
    c_exit_code = row["c exit code"]

    p_id = row["p id"]
    p_trade = row["p trade"]
    p_code_1 = row["p code 1"]
    put_op_sym = row["put op sym"]
    p_buy_at = row["p buy at"]
    p_buy_t = row["p buy t"]
    #p_buy_t = datetime.datetime.fromisoformat(p_buy_t)
    p_ltp = row["p ltp"]
    p_r_profit = row["p run pro"]
    p_b_profit = row["p book pro"]
    p_max_hi = row["p max"]
    p_exit_s = row["p exit s"]
    p_exit_at = row["p exit at"]
    p_exit_t = row["p exit time"]
    #p_exit_t = datetime.datetime.fromisoformat(p_exit_t)
    p_mes = row["p message"]
    p_exit_code = row["p exit code"]
    c_entry = row["c entry"]
    p_entry = row["p entry"]
    call_st_price = row["call st price"]
    put_st_price = row["put st price"]

    data =[indices,algo,lot,c_id,c_trade,c_code_1,call_op_sym,c_buy_at,c_buy_t,c_ltp,c_r_profit,c_b_profit,
              c_max_hi,c_exit_s,c_exit_at,c_exit_t,c_mes,c_exit_code,
              p_id,p_trade,p_code_1,put_op_sym,p_buy_at,p_buy_t,p_ltp,p_r_profit,p_b_profit,
              p_max_hi,p_exit_s,p_exit_at,p_exit_t,p_mes,p_exit_code,c_entry,p_entry,call_st_price,put_st_price]
    return data

def start_stk(indices):
    response = supabase.table("stock_data").select("*").eq("sym", indices).execute()
    data = response.data

    row = data[0]  # first matching row
    id_val = row["id"]
    indices = row["sym"]
    algo = row["algo"]
    lot = row["lot"]
    c_id = row["c_id"]
    c_trade = row["c_trade"]
    c_code_1 = row["c_code_1"]
    call_op_sym = row["call_op_sym"]
    c_buy_at = row["c_buy_at"]
    c_buy_t = row["c_buy_t"]
    #c_buy_t = datetime.datetime.fromisoformat(c_buy_t)
    c_ltp = row["c_ltp"]
    c_r_profit = row["c_run_pro"]
    c_b_profit = row["c_book_pro"]
    c_max_hi = row["c_max"]
    c_exit_s = row["c_exit_s"]
    c_exit_at = row["c_exit_at"]
    c_exit_t = row["c_exit_time"]
    #c_exit_t = datetime.datetime.fromisoformat(c_exit_t)
    c_mes = row["c_message"]
    c_exit_code = row["c_exit_code"]

    p_id = row["p_id"]
    p_trade = row["p_trade"]
    p_code_1 = row["p_code_1"]
    put_op_sym = row["put_op_sym"]
    p_buy_at = row["p_buy_at"]
    p_buy_t = row["p_buy_t"]
    #p_buy_t = datetime.datetime.fromisoformat(p_buy_t)
    p_ltp = row["p_ltp"]
    p_r_profit = row["p_run_pro"]
    p_b_profit = row["p_book_pro"]
    p_max_hi = row["p_max"]
    p_exit_s = row["p_exit_s"]
    p_exit_at = row["p_exit_at"]
    p_exit_t = row["p_exit_time"]
    #p_exit_t = datetime.datetime.fromisoformat(p_exit_t)
    p_mes = row["p_message"]
    p_exit_code = row["p_exit_code"]

    data =[indices,algo,lot,c_id,c_trade,c_code_1,call_op_sym,c_buy_at,c_buy_t,c_ltp,c_r_profit,c_b_profit,
              c_max_hi,c_exit_s,c_exit_at,c_exit_t,c_mes,c_exit_code,
              p_id,p_trade,p_code_1,put_op_sym,p_buy_at,p_buy_t,p_ltp,p_r_profit,p_b_profit,
              p_max_hi,p_exit_s,p_exit_at,p_exit_t,p_mes,p_exit_code]
    return data
def read_token():
    response = supabase.table("token_data").select("*").eq("id", 1).execute()
    data = response.data
    row = data[0]  # first matching row
    token = row["token_details"]
    return token
def get_token():
    response = (
        supabase
        .table("app_token")
        .select("token")
        .eq("id", 1)
        .single()
        .execute()
    )
    return response.data["token"]

def greater_than_zero(total): 
    if(total and total <= 0):
        raise ValueError
    return total

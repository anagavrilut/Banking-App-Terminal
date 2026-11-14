tranzactii = []
undo_list = []

def sold_curent():
    sold = 0

    for t in tranzactii:
        if t["tip"] == "intrare":
            sold += t["suma"]
        else:
            sold -= t["suma"]

    return sold
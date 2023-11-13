"""
protfolio = {
    Ticker : $ amount,
    Ticker : $ amount,
    Ticker : $ amount
}

"""


#### High Diverse Portfolio ####
HDp1 = {
    "TSLA" : 1000,
    "AAPL" : 1000,
    "COO" : 1000,
}

HDp2 = {
    "BAC" : 1000,
    "KO" : 1000,
    "KHC" : 1000,
    "AAPL" : 1000,
    "WFC" : 1000
}


# very diverse
HDp3 = {
    "AAPL" : 1000,
    "JNJ" : 1000,
    "DIS" : 1000,
    "JPM" : 1000,
    "PG" : 1000,
    "XOM" : 1000,
    "HD" : 1000,
    "VZ" : 1000,
    "KO" : 1000,
    "MMM" : 1000,
}



#### Mid Diverse Portfolio ####

# two stock different industry
MDp1 = {
    "TSLA" : 5000,
    "COO" : 5000,
}

# lots of same industry with one different
MDp2 = {
    "TSLA" : 1000,
    "DE" : 1000,
    "GM" : 1000,
    "COO" : 3000,
}

# different industry with different value
MDp3 = {
    "JNJ" : 1000,
    "AAPL" : 1000,
    "DIS" : 2000,
    "JPM" : 1500,
    "PG" : 2000,
}

# same industry with different value
MDp4 = {
    "AMZN" : 1000,
    "META" : 2000,
    "GOOGL" : 3000,
    "NFLX" : 4000,
}

#### Low Diverse Portfolio ####

# one stock
LDp1 = {
    "TSLA" : 5000,
}

# heavy on one stock
LDp2 = {
    "TSLA" : 5000,
    "AAPL" : 10,
    "COO" : 10,
}

# automobile industry
LDp3 = {
    "TSLA" : 5000,
    "DE" : 5000,
    "GM" : 5000,
}

# tech industry
LDp4 = {
    "AMZN" : 5000,
    "META" : 5000,
    "GOOGL" : 5000,
    "NFLX" : 5000,
}

# bank industry
LDp5 = {
    "BAC" : 5000,
    "JPM" : 5000,
    "WFC" : 5000,
    "C" : 5000,
    "GS" : 5000,
}


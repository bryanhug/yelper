CREATE TABLE cities(
    city_name VARCHAR(40) NOT NULL,
    PRIMARY KEY(city_name)
);

CREATE TABLE business(
    city_name VARCHAR(40) NOT NULL,
    alias VARCHAR(40) NOT NULL,
    phone VARCHAR(20),
    addr VARCHAR(40) NOT NULL,
    yelp_url VARCHAR(100) NOT NULL,
    PRIMARY KEY(alias, addr, yelp_url)
);

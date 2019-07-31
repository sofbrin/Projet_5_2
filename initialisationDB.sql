CREATE DATABASE IF NOT EXISTS purbeurre2 CHARACTER SET 'utf8';

CREATE TABLE IF NOT EXISTS CategoryDb (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
)
ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS ProductDb (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(255) NOT NULL,
    origin TEXT NOT NULL,
    manufacturing_places TEXT NOT NULL,
    countries VARCHAR(255) NOT NULL,
    store VARCHAR(255) NOT NULL,
    nutriscore CHAR(1) NOT NULL,
    url VARCHAR(255) NOT NULL,
    category SMALLINT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_category_CategoryDb
    	FOREIGN KEY(category)
    	REFERENCES CategoryDb(id)
)
ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS HistoricDb (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    product_original SMALLINT UNSIGNED NOT NULL,
    product_replaceable SMALLINT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_original_ProductDb
    	FOREIGN KEY (product_original)
    	REFERENCES ProductDb(id),
    CONSTRAINT fk_replaceable_ProductDb
    	FOREIGN KEY (product_replaceable)
    	REFERENCES ProductDb(id)
)
ENGINE=INNODB;

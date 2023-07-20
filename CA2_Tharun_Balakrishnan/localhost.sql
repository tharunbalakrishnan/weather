create schema `weather_data_schema`;

CREATE TABLE `weather_data_schema`.`weather_data` (
  `address` varchar(256) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  `maxt` float DEFAULT NULL,
  `mint` float DEFAULT NULL,
  `temp` float DEFAULT NULL,
  `precip` float DEFAULT NULL,
  `wspd` float DEFAULT NULL,
  `wdir` float DEFAULT NULL,
  `wgust` float DEFAULT NULL,
  `pressure` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
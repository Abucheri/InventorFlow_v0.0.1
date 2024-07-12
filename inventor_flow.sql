-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: flask_auth_system_demo
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf16;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES ('60034af4-7a77-489f-89db-0512d189d58e','Beverges',NULL,NULL),('645dcabc-b2ec-4b62-912c-43fa8ae87cab','Canned Goods',NULL,NULL),('65f7d1cc-9cdf-4ec6-8e0f-d3d4793e83cd','Fish & Sea Food',NULL,NULL),('68528c33-ef20-4b92-a086-c3255b7226b8','Meat',NULL,NULL),('6d59b1b0-436f-49d2-bbb7-9ebcf71b758a','Condiments & Spices',NULL,NULL),('7374870b-305c-461e-a55b-272101a0281f','Snacks',NULL,NULL),('9e044a8b-2e4f-4ab9-a000-c8d13cb394c2','Shoes','2024-07-11 16:19:09',NULL),('b2647785-ed69-4231-9c6e-0dfa09b33eb5','Vegetbles',NULL,NULL),('b5b5f810-8327-4656-9f15-0642859b56e9','Fruits',NULL,NULL),('ba31dff3-2fc4-458f-b866-61479346fd0e','Spices','2024-07-11 16:18:58',NULL),('c7e993ef-3a0e-4473-8659-a7ad64bf826a','Deli',NULL,NULL),('d4641862-fb1f-482c-b9fa-08e6d2a8c748','new cat','2024-07-12 10:33:07',NULL),('d7f37ea8-e7cc-4bde-bc3b-f5d8e63e5082','Dairy',NULL,NULL),('f618ca9c-8a00-4016-8efe-5595947e0fd3','Fish','2024-07-12 11:20:14',NULL);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` varchar(255) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `product_category_id` varchar(255) NOT NULL,
  `product_unit_id` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL DEFAULT '0.00',
  `quantity` int NOT NULL DEFAULT '0',
  `product_supplier_id` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `supplier_id_idx` (`product_supplier_id`),
  KEY `unit_id_idx` (`product_unit_id`),
  KEY `category_id` (`product_category_id`),
  CONSTRAINT `category_id` FOREIGN KEY (`product_category_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `supplier_id` FOREIGN KEY (`product_supplier_id`) REFERENCES `suppliers` (`id`),
  CONSTRAINT `unit_id` FOREIGN KEY (`product_unit_id`) REFERENCES `units` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES ('051faca4-f48e-400f-9b2d-364419259e38','Apples','b5b5f810-8327-4656-9f15-0642859b56e9','efa9e207-ebe5-4f1c-b8c6-f1167dc1ce4b','Apples',25.00,500,'7d3c702a-329b-4735-85a2-0eea55f79e15','2024-07-11 16:05:00',NULL),('09ed30c2-18e4-4362-a972-0c3eba52dae1','Cheese','d7f37ea8-e7cc-4bde-bc3b-f5d8e63e5082','efa9e207-ebe5-4f1c-b8c6-f1167dc1ce4b','wtgaegyt',50.00,200,'66797280-5b17-4be8-94c8-81f6b4cddd94','2024-07-10 23:00:00',NULL),('a9d93997-8b76-4bdf-9052-ffbff066f8f4','vfsS','645dcabc-b2ec-4b62-912c-43fa8ae87cab','8f5b1880-a30f-490e-bc57-266960a3054b','dzbn',67.00,5,'6de793c3-c1c1-47c8-b7c2-3a90c96613a0','2024-07-04 05:45:00',NULL),('cfaca7c5-5310-4127-81de-d419edbe6a7c','New product 2','f618ca9c-8a00-4016-8efe-5595947e0fd3','8f5b1880-a30f-490e-bc57-266960a3054b','Tuna samples',200.00,1000,'7d3c702a-329b-4735-85a2-0eea55f79e15','2024-07-11 15:00:00',NULL),('e1f0b213-24e8-4568-b00c-0acc4c7e10e5','Macadamia Milk','7374870b-305c-461e-a55b-272101a0281f','efa9e207-ebe5-4f1c-b8c6-f1167dc1ce4b','macadamia milk',40.00,700,'66797280-5b17-4be8-94c8-81f6b4cddd94','2024-07-10 18:47:00',NULL);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers` (
  `id` varchar(255) NOT NULL,
  `supplier_name` varchar(255) NOT NULL,
  `supplier_contact` varchar(255) NOT NULL,
  `supplier_agreement` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
INSERT INTO `suppliers` VALUES ('0815bd8b-82e4-4a83-9112-031a98297a64','hhfsfhsl','63536673645','fa vbg bn jny ','2024-07-10 12:00:00',NULL),('2d437b7d-c3a9-4632-ad4f-2ec6aada3afc','Abucheri','07969685685','1 year milk supply contract','2024-07-10 02:40:00','2024-07-10 03:36:00'),('66797280-5b17-4be8-94c8-81f6b4cddd94','Milkyland','98079685','2 year contract for yoghurt supply','2024-07-10 03:39:00',NULL),('6de793c3-c1c1-47c8-b7c2-3a90c96613a0','O\'Brien','078655552367','7 month contract for cheese','2024-07-10 02:36:00','2024-07-10 03:37:02'),('7d3c702a-329b-4735-85a2-0eea55f79e15','O\'Brien Inco.','98795639579475','fsgdshbfnhfnd','2024-07-11 12:00:00',NULL),('8da3fd24-9829-4bf4-b550-6e652a13b799','ABC Ltd. 3','53467474','ghxdnd ndj','2024-07-10 15:23:00',NULL),('9b1b5259-8881-47b0-bf07-230c66772567','ABC Ltd.','098765432','1 year contract for Meat supply','2024-07-09 04:07:00',NULL),('b59b1177-5261-40fc-83de-218fddbc6dcc','ABC Ltd. 2','42356478855','fbhnkmlo8;i','2024-07-08 13:09:00',NULL),('c965f479-afae-4e26-8221-493c0a7418bb','0\'Brien Corporate','13243543646','another awesome company\r\n            ','2024-05-11 14:56:00','2024-07-12 12:27:39'),('e25792ff-4bda-4821-9496-20c579894965','Abucheri 1','252q46457568','bhuim;o,;pou','2024-07-08 23:00:00',NULL),('ea351ed2-a7ca-4286-8888-67828fbd7250','0\'Brien Inc.','0718218398','svybujenkrnyhn','2024-07-10 13:00:00',NULL);
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL DEFAULT '0.00',
  `quantity` int NOT NULL DEFAULT '0',
  `supplier_name_id` varchar(255) NOT NULL,
  `returned` enum('YES','NO') NOT NULL DEFAULT 'NO',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_supplier_id_idx` (`supplier_name_id`),
  CONSTRAINT `product_supplier_id` FOREIGN KEY (`supplier_name_id`) REFERENCES `suppliers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (11,'Apples',25.00,500,'7d3c702a-329b-4735-85a2-0eea55f79e15','NO','2024-07-12 16:05:25',NULL),(12,'Cheese',50.00,200,'66797280-5b17-4be8-94c8-81f6b4cddd94','NO','2024-07-12 16:06:59',NULL),(13,'vfsS',67.00,5,'6de793c3-c1c1-47c8-b7c2-3a90c96613a0','NO','2024-07-12 16:07:48',NULL);
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `units`
--

DROP TABLE IF EXISTS `units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `units` (
  `id` varchar(255) NOT NULL,
  `unit` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `units`
--

LOCK TABLES `units` WRITE;
/*!40000 ALTER TABLE `units` DISABLE KEYS */;
INSERT INTO `units` VALUES ('1e8455e8-af79-4e22-869c-4685f8831d16','My Unit','2024-07-11 16:55:59',NULL),('2f94cec3-b2a7-48b3-8275-84be1530e622','Another Unit','2024-07-11 16:56:12',NULL),('346d7829-f68d-4ebb-b16b-eaa5846a082f','MLs',NULL,'2024-07-09 20:01:09'),('608a6350-1715-4aff-ac41-c7761799b0de','Tonnes','2024-07-09 20:00:50',NULL),('60f71edb-f540-4440-97b0-7f9b5bf9b8ec','Same as other','2024-07-11 16:56:23','2024-07-11 16:56:52'),('80aee4da-27fb-442f-aa66-8b2e726a8ebd','PIECES',NULL,NULL),('8834494c-94af-429a-ab1a-63f7ca7fbe65','Metre','2024-07-12 11:41:46',NULL),('8f00ae9e-2484-4ecb-9638-a8fe2a327eae','Lbs','2024-07-09 20:01:42',NULL),('8f5b1880-a30f-490e-bc57-266960a3054b','BOXES',NULL,NULL),('9cc366ad-4c97-48ba-b668-cdb9152eeed7','LTRS',NULL,NULL),('a945b7f2-d013-404d-ac43-b9c8a681a887','PKTS',NULL,NULL),('c49efd2b-d660-4565-a040-f6a348e762ae','KG',NULL,NULL),('efa9e207-ebe5-4f1c-b8c6-f1167dc1ce4b','GRAMS',NULL,NULL);
/*!40000 ALTER TABLE `units` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','user') NOT NULL DEFAULT 'user',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('0d892dc4-2b56-42aa-b365-2f23c10849eb','O\'Brien','admin@admin.com','scrypt:32768:8:1$g1TtUpv4EySR1xHS$f414c5dbdb760f734f52c35bd1e4497715443eded17037b5d7d7a14d1aa508b794b0c63e1d4d6f5670d404999631b94f10c28b66378b85f69428c84e935192df','admin'),('49d1ad35-4432-456a-8640-9535f6503186','Brian','ao@ao.com','scrypt:32768:8:1$iJJVIRJUoXme2YT4$f1dc2e120902114cd969f69ce0a9c7579ce061a5dd90660f3558ad67f5e1fb0d5e8c92cd8757a41f0721451556050149b6f5d2dc2a463efd4602c373c03fa3d9','user'),('cce676e4-0c63-4f87-9772-422247a20ab7','AOM AOM','aom@aom.com','scrypt:32768:8:1$OJwMrL8lVPTyOkuT$3cc221a6d87b86995420e35c3234949258d748876e4adf74bf4df5fdfa9051ed6fcce7cdc0e286668241cce660f8c28c3d06686a88119e310fb9742780059d47','user');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-12 16:27:39

-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: clinicalcase
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `clinicalcase`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `clinicalcase` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;

USE `clinicalcase`;

--
-- Table structure for table `ecg_findings`
--

DROP TABLE IF EXISTS `ecg_findings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ecg_findings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `examination_id` int(11) NOT NULL,
  `sinus_rhythm` varchar(30) DEFAULT NULL,
  `heart_rate` varchar(30) DEFAULT NULL,
  `p_axis` varchar(30) DEFAULT NULL,
  `qrs_axis` varchar(30) DEFAULT NULL,
  `pr_interval` varchar(30) DEFAULT NULL,
  `qtc_interval` varchar(30) DEFAULT NULL,
  `qrs_duration` varchar(30) DEFAULT NULL,
  `atrial_enlargement` varchar(100) DEFAULT NULL,
  `bundle_branch_block` varchar(50) DEFAULT NULL,
  `ventricular_hypertrophy` varchar(100) DEFAULT NULL,
  `st_segment` varchar(50) DEFAULT NULL,
  `rvh_pressure_overload` varchar(50) DEFAULT NULL,
  `additional_observations` text DEFAULT NULL,
  `ra_enlargement_ecg` varchar(50) DEFAULT NULL,
  `la_enlargement_ecg` varchar(50) DEFAULT NULL,
  `lvh_volume_overload` varchar(50) DEFAULT NULL,
  `rvh_volume_overload` varchar(50) DEFAULT NULL,
  `bv_hypertrophy` varchar(50) DEFAULT NULL,
  `lvh_pressure_overload` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `examination_id` (`examination_id`),
  CONSTRAINT `ecg_findings_ibfk_1` FOREIGN KEY (`examination_id`) REFERENCES `examinations` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecg_findings`
--

LOCK TABLES `ecg_findings` WRITE;
/*!40000 ALTER TABLE `ecg_findings` DISABLE KEYS */;
INSERT INTO `ecg_findings` VALUES (1,6,'Present','75','42.9','33.9','31.9','213','221.9',NULL,'Left BBB',NULL,'Normal','20',NULL,'Present','Present','Present','Absent','Present','60–140 BPM'),(2,16,'Present','Below 60 BPM','Present','LAD','34','23','Below 80 ms',NULL,'Left BBB',NULL,'Increased',NULL,NULL,'Present','Present','Present','Present','Present',NULL);
/*!40000 ALTER TABLE `ecg_findings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `examinations`
--

DROP TABLE IF EXISTS `examinations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `examinations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` int(11) NOT NULL,
  `examination_type` varchar(30) NOT NULL,
  `examination_date` date NOT NULL,
  `status` varchar(30) NOT NULL DEFAULT 'DRAFT',
  `clinical_observations` text DEFAULT NULL,
  `clinical_impression` text DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `xray_findings` text DEFAULT NULL,
  `xray_measurements` text DEFAULT NULL,
  `xray_notes` text DEFAULT NULL,
  `ecg_findings` text DEFAULT NULL,
  `ecg_measurements` text DEFAULT NULL,
  `ecg_notes` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `examinations_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`),
  CONSTRAINT `examinations_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `examinations`
--

LOCK TABLES `examinations` WRITE;
/*!40000 ALTER TABLE `examinations` DISABLE KEYS */;
INSERT INTO `examinations` VALUES (1,1,'CHEST_XRAY','2026-10-12','PENDING_REVIEW',NULL,NULL,1,'2026-10-12 15:27:26',NULL,NULL,NULL,NULL,NULL,NULL),(6,1,'ECG','2026-10-13','PENDING_REVIEW',NULL,NULL,1,'2026-10-13 06:16:35',NULL,NULL,NULL,NULL,NULL,NULL),(15,2,'CHEST_XRAY','2026-10-13','PENDING_REVIEW',NULL,NULL,1,'2026-10-13 08:47:36',NULL,NULL,NULL,NULL,NULL,NULL),(16,2,'ECG','2026-10-13','PENDING_REVIEW',NULL,NULL,1,'2026-10-13 09:15:06',NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `examinations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` varchar(20) NOT NULL,
  `full_name` varchar(150) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `sex` varchar(20) DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `clinical_indication` text DEFAULT NULL,
  `address` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `patient_id` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (1,'PT-0001','Vishal Prajapati Rudra','2026-10-12','Male','9616260210','loveindiabyvishal9616@gmail.com',NULL,'Gadhaseni\r\n26','2026-10-12 15:12:20'),(2,'PT-0002','rahul','2016-05-24','Male','714874172218432','loveindiabyvishal9616@gmail.com',NULL,'Gadhaseni\r\n26','2026-10-13 06:02:39');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` varchar(30) NOT NULL DEFAULT 'DOCTOR',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Vishal Prajapati','admin','scrypt:32768:8:1$FjBb6ClYUSwYegyf$6b1dd89a5a012140ffe706447bdeaa9fa950b0338e99e46f9bf42672bf73d99f0ec0c440f725a1d0c4a527efa819fe1d8c07cd3913d3644a292859c544f45f13','SUPER_ADMIN','2026-10-12 14:57:05');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xray_findings`
--

DROP TABLE IF EXISTS `xray_findings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xray_findings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `examination_id` int(11) NOT NULL,
  `rotation` varchar(30) DEFAULT NULL,
  `inspiratory_film` varchar(30) DEFAULT NULL,
  `penetration` varchar(30) DEFAULT NULL,
  `situs` varchar(30) DEFAULT NULL,
  `cardiac_position` varchar(30) DEFAULT NULL,
  `cardiomegaly` varchar(30) DEFAULT NULL,
  `ctr_percent` float DEFAULT NULL,
  `chamber_enlargement` varchar(150) DEFAULT NULL,
  `artery_dilatation` varchar(150) DEFAULT NULL,
  `pulmonary_pattern` varchar(100) DEFAULT NULL,
  `pah_pvh` varchar(100) DEFAULT NULL,
  `additional_notes` text DEFAULT NULL,
  `ra_enlargement` varchar(50) DEFAULT NULL,
  `la_enlargement` varchar(50) DEFAULT NULL,
  `rv_enlargement` varchar(50) DEFAULT NULL,
  `lv_enlargement` varchar(50) DEFAULT NULL,
  `aorta_position_knuckle` varchar(50) DEFAULT NULL,
  `thymic_shadow` varchar(50) DEFAULT NULL,
  `aa_dilatation` varchar(50) DEFAULT NULL,
  `da_dilatation` varchar(50) DEFAULT NULL,
  `mpa_dilatation` varchar(50) DEFAULT NULL,
  `rpa_dilatation` varchar(50) DEFAULT NULL,
  `lpa_dilatation` varchar(50) DEFAULT NULL,
  `pulmonary_plethora` varchar(50) DEFAULT NULL,
  `pulmonary_oligemia` varchar(50) DEFAULT NULL,
  `pah` varchar(50) DEFAULT NULL,
  `pvh` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `examination_id` (`examination_id`),
  CONSTRAINT `xray_findings_ibfk_1` FOREIGN KEY (`examination_id`) REFERENCES `examinations` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xray_findings`
--

LOCK TABLES `xray_findings` WRITE;
/*!40000 ALTER TABLE `xray_findings` DISABLE KEYS */;
INSERT INTO `xray_findings` VALUES (1,1,'Absent','Yes','Underpenetrated','Situs Solitus','Levocardia','Present',75,'RA','None reported','Plethora','PAH features','dsdaSDd',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,15,'Present','Yes','Normal','Solitus','Dextrocardia','Present',NULL,NULL,NULL,NULL,NULL,NULL,'Present','Present','Present','Present','Left','Present','Absent','Absent','Present','Present','Present','Present','Present','Present','Present');
/*!40000 ALTER TABLE `xray_findings` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-13 16:32:31

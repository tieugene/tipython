-- Updating DB from 0.9 to 1.0
ALTER TABLE `sro2_sro` ADD COLUMN `displayname` VARCHAR(40)  NOT NULL;
ALTER TABLE `sro2_sro` ADD COLUMN `address` VARCHAR(255)  NOT NULL;

ALTER TABLE `sro2_sro`
	DROP COLUMN `name`,
	DROP COLUMN `fullname`,
	ADD COLUMN `name_id` INTEGER UNSIGNED NOT NULL,
	ADD COLUMN `fillname_id` INTEGER UNSIGNED NOT NULL;

ALTER TABLE `sro2_sroown`
	ADD COLUMN `effectorfull` INTEGER UNSIGNED NOT NULL,
	ADD COLUMN `managefull` INTEGER UNSIGNED NOT NULL,
	ADD COLUMN `managedeputyfull` INTEGER UNSIGNED NOT NULL,
	ADD COLUMN `manage` INTEGER UNSIGNED NOT NULL,
	ADD COLUMN `effector` INTEGER UNSIGNED NOT NULL,
	ADD COLUMN `managechief` INTEGER UNSIGNED NOT NULL,
	ADD COLUMN `signdeputy` INTEGER UNSIGNED NOT NULL;

DELETE FROM `sro2_sro` WHERE 1=1;

DELETE FROM `sro2_sroown` WHERE 1=1;

-- MySQL dump 10.13  Distrib 5.1.49, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: lansite
-- ------------------------------------------------------
-- Server version	5.1.49-1ubuntu8.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `gw_wordcombination`
--

DROP TABLE IF EXISTS `gw_wordcombination`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gw_wordcombination` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nominative` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `genetive` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `dative` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `accusative` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `instrumental` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `prepositional` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nominative` (`nominative`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gw_wordcombination`
--

LOCK TABLES `gw_wordcombination` WRITE;
/*!40000 ALTER TABLE `gw_wordcombination` DISABLE KEYS */;
INSERT INTO `gw_wordcombination` VALUES (16,'НП «СтройПартнер»','','','','',''),(17,'Некоммерческое партнерство инженеров-изыскателей «СтройПартнер»','','','','',''),(18,'НП СРО «МООАСП»','','','','',''),(19,'Некоммерческое партнерство саморегулируемая организация «Межрегиональное объединение организаций архитектурно - строительного проектирования»','','','','',''),(20,'Исполнительный директор','','','','',''),(21,'Правление','','','','',''),(22,'Председатель','','','','',''),(23,'НП СРО «МООЖС»','','','','',''),(24,'Некоммерческое партнерство саморегулируемая организация «Межрегиональное объединение организаций железнодорожного строительства»','','','','','');
/*!40000 ALTER TABLE `gw_wordcombination` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-12-07 14:19:27

-- MySQL dump 10.13  Distrib 5.1.49, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: lansite
-- ------------------------------------------------------
-- Server version	5.1.49-1ubuntu8.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `sro2_sro`
--

DROP TABLE IF EXISTS `sro2_sro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sro2_sro` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `regno` varchar(20) NOT NULL,
  `type_id` int(10) unsigned NOT NULL,
  `own` tinyint(1) NOT NULL,
  `displayname` varchar(40) NOT NULL,
  `address` varchar(255) NOT NULL,
  `name_id` int(10) unsigned NOT NULL,
  `fullname_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `regno` (`regno`),
  KEY `sro2_sro_777d41c8` (`type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sro2_sro`
--

LOCK TABLES `sro2_sro` WRITE;
/*!40000 ALTER TABLE `sro2_sro` DISABLE KEYS */;
INSERT INTO `sro2_sro` VALUES (2,'СРО-П-115-18012010',2,1,'МООАСП','191040, г.Санкт-Петербург, ул. Марата, д.42',18,19),(1,'СРО-С-043-28092009',3,1,'МООЖС','191040, г.Санкт-Петербург, ул. Марата, д.42',23,24),(3,'СРО-И-028-13052010',1,0,'СтройПартнер','192012 г. Санкт-Петербург переулок Рабфаковский  3-й, д. 5, корпус 4, литер А, офис 1-10',16,17);
/*!40000 ALTER TABLE `sro2_sro` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-12-07 14:11:28

-- MySQL dump 10.13  Distrib 5.1.49, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: lansite
-- ------------------------------------------------------
-- Server version	5.1.49-1ubuntu8.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `sro2_sroown`
--

DROP TABLE IF EXISTS `sro2_sroown`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sro2_sroown` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sro_id` int(11) NOT NULL,
  `boss` varchar(20) NOT NULL,
  `bosstitle` varchar(50) NOT NULL,
  `tplprefix` varchar(10) NOT NULL,
  `ftp` varchar(50) DEFAULT NULL,
  `path` varchar(100) DEFAULT NULL,
  `sshhost` varchar(50) DEFAULT NULL,
  `effectorfull_id` int(10) unsigned NOT NULL,
  `managefull_id` int(10) unsigned NOT NULL,
  `managedeputyfull_id` int(10) unsigned NOT NULL,
  `signdeputy` tinyint(1) NOT NULL,
  `manage_id` int(10) unsigned NOT NULL,
  `effector_id` int(10) unsigned NOT NULL,
  `managechief_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sro_id` (`sro_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sro2_sroown`
--

LOCK TABLES `sro2_sroown` WRITE;
/*!40000 ALTER TABLE `sro2_sroown` DISABLE KEYS */;
INSERT INTO `sro2_sroown` VALUES (2,2,'В.А. Сасалин','Заместитель Председателя Правления','mooasp','ftp.moozs.ru','mooasp.ru/docs/joom/images/stories/docs','ssh.npsts.nichost.ru',0,0,0,0,0,0,0),(1,1,'В.А.Силкин','Заместитель  Председателя Правления','moozs','ftp.moozs.ru','moozs.ru/docs/joom/images','ssh.npsts.nichost.ru',0,0,0,0,0,0,0),(3,3,'Алешина М. С.','','mooasp',NULL,NULL,NULL,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `sro2_sroown` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-12-07 14:11:51

-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: tradrdv_db
-- ------------------------------------------------------
-- Server version	5.7.38-log

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('8720fb320327');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat`
--

DROP TABLE IF EXISTS `chat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `receiver_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `last_chat` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_chat_receiver_id` (`receiver_id`),
  CONSTRAINT `chat_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat`
--

LOCK TABLES `chat` WRITE;
/*!40000 ALTER TABLE `chat` DISABLE KEYS */;
INSERT INTO `chat` VALUES (1,1,10,'2022-09-28 09:11:36'),(2,1,15,'2022-09-22 03:26:29'),(3,1,11,'2022-09-22 03:26:51'),(4,2,19,'2022-09-21 11:17:32'),(5,1,2,'2022-10-04 13:41:17'),(6,2,10,'2022-09-19 20:09:52'),(7,2,4,'2022-09-19 21:54:17'),(8,19,10,'2022-09-28 09:17:27'),(9,2,8,'2022-09-25 11:32:25'),(10,3,2,'2022-10-18 10:53:41'),(11,2,29,'2022-09-22 06:04:09'),(12,1,23,'2022-09-29 11:39:09'),(13,2,27,'2022-09-26 07:59:11'),(14,2,18,'2022-09-27 09:05:59'),(15,2,5,'2022-11-28 18:10:54'),(16,2,12,'2022-09-28 18:05:43'),(17,1,36,'2022-10-05 11:16:04'),(18,2,36,'2022-10-05 11:08:03'),(19,18,44,'2022-10-08 19:29:15'),(20,2,9,'2022-10-08 23:58:28'),(21,2,24,'2022-10-11 05:11:34'),(22,2,22,'2022-10-13 08:35:32'),(23,2,49,'2022-11-22 14:41:29'),(24,1,3,'2022-10-21 05:13:17'),(25,5,51,'2022-10-23 09:26:13'),(26,2,52,'2022-11-06 16:02:26'),(27,1,52,'2022-11-06 18:25:59'),(28,1,53,'2022-11-13 21:46:11'),(29,4,15,'2022-11-09 20:40:56'),(30,2,26,'2022-12-04 08:53:10'),(31,2,23,'2022-11-13 21:46:46'),(32,2,56,'2022-11-23 09:24:21'),(33,1,49,'2022-11-22 13:53:08'),(34,1,26,'2022-12-05 13:25:13');
/*!40000 ALTER TABLE `chat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `trad_id` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `avis` varchar(200) NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `commercial`
--

DROP TABLE IF EXISTS `commercial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `commercial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CCP_number` varchar(64) DEFAULT NULL,
  `BaridiMob_RIP` varchar(64) DEFAULT NULL,
  `ePayment_type` varchar(32) DEFAULT NULL,
  `e_Payment` varchar(64) DEFAULT NULL,
  `id_card` varchar(500) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_commercial_timestamp` (`timestamp`),
  CONSTRAINT `commercial_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commercial`
--

LOCK TABLES `commercial` WRITE;
/*!40000 ALTER TABLE `commercial` DISABLE KEYS */;
/*!40000 ALTER TABLE `commercial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `receiver_id` int(11) NOT NULL,
  `message` varchar(1000) DEFAULT NULL,
  `file` varchar(500) DEFAULT NULL,
  `file_statut` tinyint(1) DEFAULT NULL,
  `read` tinyint(1) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_contact_receiver_id` (`receiver_id`),
  KEY `ix_contact_id` (`id`),
  CONSTRAINT `contact_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=158 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact`
--

LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
INSERT INTO `contact` VALUES (1,1,'Nouveau contact',NULL,0,0,'2022-09-15 12:27:57',10),(2,10,'Bonjour Yazid, veuillez compléter votre inscription en allant de votre compte vers la partie : devenir un traducteur... merci ! ',NULL,0,0,'2022-09-15 12:58:20',1),(3,1,'Nouveau contact',NULL,0,0,'2022-09-15 15:43:08',15),(4,1,'Nouveau contact',NULL,0,0,'2022-09-15 15:43:26',15),(5,1,'Nouveau contact',NULL,0,0,'2022-09-15 18:16:00',11),(6,1,'Nouveau contact',NULL,0,0,'2022-09-15 18:16:33',11),(7,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-09-15 22:14:10',19),(8,1,'Nouveau contact',NULL,0,0,'2022-09-16 01:53:18',2),(9,19,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-09-16 02:50:19',2),(10,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-09-16 14:32:36',10),(11,2,NULL,'assets/images/message_file/1663338858.924103FB_IMG_1654091237175.jpg',1,0,'2022-09-16 14:34:19',10),(12,1,'C\'est, j\'attends votre confirmation ',NULL,0,0,'2022-09-16 14:36:58',10),(13,2,'J\'attends votre confirmation ',NULL,0,0,'2022-09-16 14:38:38',10),(14,1,'Nouveau contact',NULL,0,0,'2022-09-16 14:53:19',2),(15,10,'Bonjour Yazid, vous avez joint les documents sur l\'inscription : devenir traducteur ?',NULL,0,0,'2022-09-16 15:00:42',1),(16,11,'Bonjour Houda\r\n, vous avez joint les documents sur l\'inscription : devenir traducteur ? ',NULL,0,0,'2022-09-16 15:01:03',1),(17,15,'Bonjour HAKO, vous avez joint les documents sur l\'inscription : devenir traducteur ? ',NULL,0,0,'2022-09-16 15:01:25',1),(18,15,'Veuillez cliquer sur : devenir traducteur, suivre les instructions envoyées sur votre e-mail ou spam... le reçu à joindre c\'est celui de l\'abonnement que vous avez payé la toute première fois, si vous ne le trouvez pas, joignez n\'importe quel document',NULL,0,0,'2022-09-16 15:03:05',1),(19,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-09-16 17:20:11',4),(20,19,'Nouveau message, je suis intéressé par votre profil. Etes vous disponible pour me renseigner?',NULL,0,0,'2022-09-16 17:51:15',10),(21,19,'Nouveau message, je suis intéressé par votre profil. Etes vous disponible pour me renseigner?',NULL,0,0,'2022-09-16 17:51:31',10),(22,10,'Bonsoir, Veuillez joindre un reçu du paiement de caution annuelle de traducteur (15000DA) et votre profil sera validé. Merci',NULL,0,0,'2022-09-16 21:01:43',2),(23,4,'Bonsoir, Veuillez joindre un reçu du paiement de caution annuelle de traducteur (15000DA) et votre profil sera validé. Merci!',NULL,0,0,'2022-09-16 21:02:12',2),(24,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-09-17 06:24:23',8),(25,2,NULL,'assets/images/message_file/1663398294.736478Recu_de_versement.pdf',1,0,'2022-09-17 07:04:55',4),(26,2,'Veuillez trouver ci-joint le reçu de paiement.\r\nSalutation,\r\n',NULL,0,0,'2022-09-17 07:07:33',4),(27,8,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-09-17 16:39:57',2),(28,8,'Bonsoir Mohand, votre profil est déjà en ligne. Mais il me faut votre bio, numéro et adresse postale. Veuillez me les envoyer aussi vite que possible',NULL,0,0,'2022-09-17 16:46:50',2),(29,3,'Nouveau message, je suis intéressé par votre profil. Etes vous disponible pour me renseigner?',NULL,0,0,'2022-09-17 16:47:40',2),(30,3,'Bonsoir Linda, votre profil est déjà en ligne. Mais il me faut votre bio, numéro, ccp et adresse postale. Veuillez me les envoyer aussi vite que possible',NULL,0,0,'2022-09-17 16:48:43',2),(31,3,'Bonsoir, veuillez joindre un reçu ccp de 15000da au lieu d\'une simple image. sauf si vous êtes déjà en contrat avec Hanane, alors veuillez me le confirmer en répondant ce message ',NULL,0,0,'2022-09-17 17:03:55',2),(32,10,'Désolé, votre reçu n\'est pas vérifié. Veuillez nous envoyer plus de détails par la discussion',NULL,0,0,'2022-09-17 17:04:09',1),(33,1,'J\'ai déjà ré-inscris et j\'ai déjà payé l\'abonnement et vous êtes au courant, alors si vous voulez vous pouvez facilement valider mon inscription et mon profil, merci, j\'ai perdu le reçu de l\'opération alors vous me demandez pas de vous en  envoyer ',NULL,0,0,'2022-09-17 17:31:06',10),(34,1,'Vous dites \" honesty is the best policy\" ',NULL,0,0,'2022-09-17 17:31:49',10),(35,2,'Bonsoir ,oui je suis en contacte avec Hanane ',NULL,0,0,'2022-09-17 19:10:48',3),(36,2,'Bio :Dynamique,ponctuel et sérieuse .\r\nCCP:Mme Bensaddek Lynda \r\n    42\r\nAddress :39Houaria Abdeljader Sakia ELhamra (Faubourg Thiers )Sidi Bel Abbes 22000',NULL,0,0,'2022-09-17 19:15:24',3),(37,2,'CCP:Mme Bensaddek Lynda \r\n0023206367    42',NULL,0,0,'2022-09-17 19:16:22',3),(38,3,'Bien reçu',NULL,0,0,'2022-09-17 20:59:02',2),(39,4,'Bonsoir, désolé Abdel pour joindre le reçu aller sur votre profil -> onglet \"Accords\" -> \"Aperçu\" (puis ajouter le reçu et ensuite enregistrer )',NULL,0,0,'2022-09-17 21:09:34',2),(40,2,'Bonjour,\r\nBien reçu. \r\n',NULL,0,0,'2022-09-18 07:28:15',4),(41,10,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-09-18 11:57:56',2),(42,10,'Bonsoir, je vous prie de nous excuser, ce n\'était pas Hanane en personne qui était en communication avec vous donc j\'ai dû vérifier les détail auprès d\'elle pour valider votre compte',NULL,0,0,'2022-09-18 12:02:13',2),(43,4,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-09-18 12:09:43',2),(44,2,'Et alors, ça veut dire qu\'il n\'est pas encore validé ?',NULL,0,0,'2022-09-18 12:56:03',10),(45,10,'Votre profil est déjà validé ',NULL,0,0,'2022-09-18 19:51:53',2),(46,2,'D\'accord alors comment ça fonctionne ?',NULL,0,0,'2022-09-18 20:27:06',10),(47,10,'Pour faire court, les clients viennent sur votre profil et vous contactent ou vous engagent pour un travail, vous discutez du prix avec le client et si tout est bon vous acceptez le deal ensuite le client paye et vous vous travaillez. vous aurez plus de details plus tard. Essayez de vous familiarisez avec votre interface de traducteur menu->gestion',NULL,0,0,'2022-09-19 19:59:17',2),(48,10,'Et aussi modifier votre profil pour avoir une image plus nette sur le site (Pays et Sex)',NULL,0,0,'2022-09-19 20:02:40',2),(49,4,'comment ça fonctionne ?',NULL,0,0,'2022-09-19 20:04:45',2),(50,4,'Pour faire court, les clients viennent sur votre profil et vous contactent ou vous engagent pour un travail, vous discutez du prix avec le client et si tout est bon vous acceptez le deal ensuite le client paye et vous vous travaillez. vous aurez plus de details plus tard. Essayez de vous familiarisez avec votre interface de traducteur menu->gestion',NULL,0,0,'2022-09-19 20:05:07',2),(51,4,'Et aussi modifier votre profil pour avoir une image plus nette sur le site (Pays et Sex)',NULL,0,0,'2022-09-19 20:05:34',2),(52,3,'comment ça fonctionne ?\r\n\r\nPour faire court, les clients viennent sur votre profil et vous contactent ou vous engagent pour un travail, vous discutez du prix avec le client et si tout est bon vous acceptez le deal ensuite le client paye et vous vous travaillez. vous aurez plus de details plus tard. Essayez de vous familiarisez avec votre interface de traducteur menu->gestion\r\n\r\nEt aussi modifier votre profil pour avoir une image plus nette sur le site (Pays et Sex)',NULL,0,0,'2022-09-19 20:07:00',2),(53,8,'comment ça fonctionne ? Pour faire court, les clients viennent sur votre profil et vous contactent ou vous engagent pour un travail, vous discutez du prix avec le client et si tout est bon vous acceptez le deal ensuite le client paye et vous vous travaillez. vous aurez plus de details plus tard. Essayez de vous familiarisez avec votre interface de traducteur menu->gestion Et aussi modifier votre profil pour avoir une image plus nette sur le site (Pays et Sex)',NULL,0,0,'2022-09-19 20:07:35',2),(54,2,'D\'accord merci ',NULL,0,0,'2022-09-19 20:09:52',10),(55,2,'Oui mais dès que je met enregistre ça me dit d’avoir un pseudo j’ai déjà un ',NULL,0,0,'2022-09-19 20:10:27',3),(56,2,'Bonjour,\r\nJ’ai essayé à maintes reprises d’actualiser les informations de mon profil (Pays, Sexe et rajout de ma photo), mais quand je click sur « Enregistrer » je reçois le message : « Veuillez fournir un nom d’utilisateur correct » (voir les captures d’écran ci-jointes). \r\nS’il vous plaît, pourriez-vous m’indiquer comment y remédier ?\r\nSalutations.',NULL,0,0,'2022-09-19 21:54:17',4),(57,2,'Bonjour Hanane ,j’espère que vous allez bien,est ce que mon profile est fonctionnel maintenant ou pas?!',NULL,0,0,'2022-09-20 06:52:13',3),(58,2,'hello',NULL,0,0,'2022-09-21 11:17:32',19),(59,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-09-21 11:37:56',29),(60,3,'le problème est résolu, veuillez réessayer, merci',NULL,0,0,'2022-09-21 11:48:06',2),(61,2,'Merciiii Hanane ',NULL,0,0,'2022-09-21 18:44:59',3),(62,15,'Bonjour Abdelhak. Nous espérons que vous allez bien. Veuillez compléter votre inscription en allant sur : devenir traducteur. merci !',NULL,0,0,'2022-09-22 03:26:29',1),(63,11,'Bonjour Houda. Nous espérons que vous allez bien. Veuillez compléter votre inscription en allant sur : devenir traducteur. merci !',NULL,0,0,'2022-09-22 03:26:51',1),(64,29,'Bonjour Marc ',NULL,0,0,'2022-09-22 06:04:09',2),(65,1,'Nouveau contact',NULL,0,0,'2022-09-22 23:12:15',23),(66,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-09-23 21:44:16',27),(67,23,'Bonjour Monsef, tu vas bien j\'espère... tu en es où avec l\'inscription ? Tu es allé sur : devenir traducteur ?',NULL,0,0,'2022-09-24 05:19:13',1),(68,1,'Bonsoir Hanane',NULL,0,0,'2022-09-24 22:49:16',23),(69,1,'Nouveau contact',NULL,0,0,'2022-09-24 23:12:06',23),(70,1,'Oui ',NULL,0,0,'2022-09-24 23:12:16',23),(71,1,'J\'ai essayé plusieurs fois ',NULL,0,0,'2022-09-24 23:12:33',23),(72,1,'Mais ça ne marche toujours pas ',NULL,0,0,'2022-09-24 23:12:55',23),(73,1,'Can you check it please ?',NULL,0,0,'2022-09-24 23:14:33',23),(74,8,'Nouveau message, je suis intéressé par votre profil. Etes vous disponible pour me renseigner?',NULL,0,0,'2022-09-25 11:32:25',2),(75,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-09-25 16:30:10',18),(76,18,'Bonsoir Sarah S, vous avez passé une étape, veuillez compléter votre inscription en joignant le reçu de paiement \r\n',NULL,0,0,'2022-09-25 18:38:19',2),(77,2,'Bonjour,\r\nVoici mon reçu de paiement ',NULL,0,0,'2022-09-25 19:12:33',18),(78,2,NULL,'assets/images/message_file/1664133269.917401Screenshot_20220925-201015_Gallery.pdf',1,0,'2022-09-25 19:14:30',18),(79,18,'Merci dear, veuillez le joindre directement sur la partie devenir traducteur à compléter...',NULL,0,0,'2022-09-25 19:28:26',2),(80,23,'Hi Monsef\r\nWhat was the last step you have undertook ? \r\n',NULL,0,0,'2022-09-25 21:23:06',1),(81,18,'Veuillez aller sur votre profil -> Accords-> Aperçu, ensuite vous ajoutez le reçu puis enregistrer ',NULL,0,0,'2022-09-26 06:21:28',2),(82,27,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-09-26 07:59:11',2),(83,1,'Nouveau contact',NULL,0,0,'2022-09-26 14:31:45',2),(84,18,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-09-27 01:26:07',2),(85,2,'Bonjour\r\nComment va se passer le travail ?\r\nQui va répartir les missions ?\r\nOu bien ça sera aux clients de choisir les traducteurs !?',NULL,0,0,'2022-09-27 09:05:59',18),(86,19,'Bonjour ',NULL,0,0,'2022-09-28 09:10:54',10),(87,1,'Nouveau contact',NULL,0,0,'2022-09-28 09:11:36',10),(88,10,'Bonjour',NULL,0,0,'2022-09-28 09:17:27',19),(89,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-09-28 12:35:06',5),(90,2,'Bonjour Hanane',NULL,0,0,'2022-09-28 12:37:21',5),(91,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-09-28 18:01:52',12),(92,12,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-09-28 18:05:43',2),(93,5,'Bonjour, veuillez ajouter le reçu de paiement accords->aperçu ',NULL,0,0,'2022-09-28 18:20:09',2),(94,1,'Hi!',NULL,0,0,'2022-09-29 11:38:44',23),(95,1,'The one before the last one',NULL,0,0,'2022-09-29 11:39:09',23),(96,5,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-10-01 22:38:12',2),(97,1,'Nouveau contact',NULL,0,0,'2022-10-03 23:58:58',36),(98,1,'Nouveau contact',NULL,0,0,'2022-10-04 11:35:25',2),(99,36,'Bonjour Adeline...\r\nVeuillez compléter votre inscription...',NULL,0,0,'2022-10-04 11:57:24',1),(100,1,'Nouveau contact',NULL,0,0,'2022-10-04 13:41:17',2),(101,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-10-04 17:21:37',36),(102,36,'Bonsoir Adeline,veuillez joindre votre reçu de paiement pour compléter votre adhésion...',NULL,0,0,'2022-10-04 21:09:56',2),(103,36,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-10-05 10:35:01',2),(104,2,'Bonjour Hanane!\r\nSorry!  J\'ai pas pu enregistrer mon reçu de paiement dans les délais. Prière de renouveler l\'accord. \r\nMerci de comprendre!\r\n\r\n',NULL,0,0,'2022-10-05 11:08:03',36),(105,1,'Nouveau contact',NULL,0,0,'2022-10-05 11:16:04',36),(106,18,'Nouveau message, je suis intéressé par votre profil. Etes vous disponible pour me renseigner?',NULL,0,0,'2022-10-08 00:47:25',44),(107,18,'Nouveau message, je suis intéressé par votre profil. Etes vous disponible pour me renseigner?',NULL,0,0,'2022-10-08 14:15:00',44),(108,44,'Bonjour,\r\nOui madame biensure. \r\nÀ votre service.',NULL,0,0,'2022-10-08 19:29:15',18),(109,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-10-08 20:52:35',9),(110,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-10-08 21:58:32',24),(111,2,'\r\n',NULL,0,0,'2022-10-08 22:10:27',24),(112,2,NULL,'assets/images/message_file/1665267029.713436recu_de_paiement.pdf',1,0,'2022-10-08 22:10:30',24),(113,2,'Bien le bonsoir, voilà le reçu de paiement (effectué depuis le compte de ma maman back then)\r\n',NULL,0,0,'2022-10-08 22:11:30',24),(114,9,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-10-08 23:58:28',2),(115,24,'Ya 3omriii, salutations à la mamaa ! From Hanane GHEDIRI.',NULL,0,0,'2022-10-11 02:01:19',2),(116,24,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-10-11 05:11:34',2),(117,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-10-11 05:42:32',22),(118,22,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-10-12 23:12:16',2),(119,2,'Enfiiiiin !\r\nmerci beaucoup :) ',NULL,0,0,'2022-10-13 08:35:32',22),(120,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-10-15 17:55:53',49),(121,2,'Bonjour',NULL,0,0,'2022-10-15 17:57:28',49),(122,2,'Bonjour hanane ',NULL,0,0,'2022-10-18 10:52:55',3),(123,2,'J’espère que tu vas bien ',NULL,0,0,'2022-10-18 10:53:15',3),(124,2,'J’essaye de te joindre mais je n’y arrive pas ',NULL,0,0,'2022-10-18 10:53:41',3),(125,2,'Comment payer la caution?',NULL,0,0,'2022-10-20 11:19:22',49),(126,1,'Nouveau contact',NULL,0,0,'2022-10-21 05:13:17',3),(127,5,'Nouveau message, je suis intéressé par votre profil. Etes vous disponible pour me renseigner?',NULL,0,0,'2022-10-23 07:45:26',51),(128,5,'Salut',NULL,0,0,'2022-10-23 07:46:03',51),(129,51,'Bonjour\r\nJe suis à votre disposition ',NULL,0,0,'2022-10-23 09:26:13',5),(130,49,'Bonjour très chère, veuillez verser 14000 Da sur le compte suivant :  Le compte CCP: GHEDIRI Hanane -   clé 96 - adresse : Tipaza\r\n\r\nSi à travers BaridiMob :496   ',NULL,0,0,'2022-10-23 14:05:23',2),(131,49,'Ensuite, nous vous guiderons sur comment vous joignez le reçu de versement à votre formulaire déjà complété partiellement, pour pouvoir vous valider votre profil...',NULL,0,0,'2022-10-23 14:06:50',2),(132,49,'Bonjour très chère, veuillez verser 14000 Da sur le compte suivant : Le compte CCP: GHEDIRI Hanane - clé 96 - adresse : Tipaza',NULL,0,0,'2022-10-23 14:07:41',2),(133,49,'Si à travers BaridiMob : 00799999000205404496   ',NULL,0,0,'2022-10-23 14:08:07',2),(134,49,'Ensuite, nous vous guiderons sur comment vous joignez le reçu de versement à votre formulaire déjà complété partiellement, pour pouvoir vous valider votre profil... ',NULL,0,0,'2022-10-23 14:08:25',2),(135,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-11-05 16:49:36',52),(136,1,'Nouveau contact',NULL,0,0,'2022-11-06 13:53:50',52),(137,52,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-11-06 16:02:26',2),(138,1,'Nouveau contact',NULL,0,0,'2022-11-06 18:25:59',52),(139,1,'Nouveau contact',NULL,0,0,'2022-11-08 11:51:59',53),(140,4,'Nouveau message, je suis intéressé par votre profil. Etes vous disponible pour me renseigner?',NULL,0,0,'2022-11-09 19:32:05',15),(141,15,'Je suis disponible. En quoi pourrais-je vous être utile ?',NULL,0,0,'2022-11-09 20:40:56',4),(142,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-11-12 09:32:37',26),(143,26,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-11-12 09:48:39',2),(144,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-11-12 12:46:08',23),(145,53,'Bonsoir Pretty Soumi ! Merci de nous avoir choisis, votre travail vous sera remis pas plus tard que le 9 Décembre...',NULL,0,0,'2022-11-13 21:44:22',1),(146,1,'Nouveau contact',NULL,0,0,'2022-11-13 21:46:08',53),(147,1,'Nouveau contact',NULL,0,0,'2022-11-13 21:46:11',53),(148,23,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-11-13 21:46:46',2),(149,2,'Nouveau accord: Paiement de caution annuelle de traducteur',NULL,0,0,'2022-11-20 19:59:46',56),(150,1,'Nouveau contact',NULL,0,0,'2022-11-22 13:53:08',49),(151,49,'Bonjour chère Dame, on n\'a ps encore reçu le document de transfert d\'argent enregistré...',NULL,0,0,'2022-11-22 14:29:55',2),(152,49,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-11-22 14:41:29',2),(153,56,'Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez TRADRDV',NULL,0,0,'2022-11-22 22:48:57',2),(154,2,'Merci je suis tres honoré',NULL,0,0,'2022-11-23 09:24:21',56),(155,5,'Nouveau message, je suis intéressé par votre profil. Etes vous disponible pour me renseigner?',NULL,0,0,'2022-11-28 18:10:54',2),(156,2,'Merci infiniment chère Hanane. Ravi d\'être parmi vous',NULL,0,0,'2022-12-04 08:53:10',26),(157,1,'Nouveau contact',NULL,0,0,'2022-12-05 13:25:13',26);
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashbord`
--

DROP TABLE IF EXISTS `dashbord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashbord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `revenu_abon` int(11) NOT NULL,
  `revenu_test` int(11) NOT NULL,
  `revenu_work` int(11) NOT NULL,
  `freelance_part` int(11) NOT NULL,
  `revenu_total` int(11) NOT NULL,
  `accueil_view` int(11) NOT NULL,
  `traducteur_view` int(11) NOT NULL,
  `remain_day` int(11) DEFAULT NULL,
  `begin` datetime DEFAULT NULL,
  `end` datetime DEFAULT NULL,
  `donation_save` int(11) NOT NULL,
  `impot_save` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashbord`
--

LOCK TABLES `dashbord` WRITE;
/*!40000 ALTER TABLE `dashbord` DISABLE KEYS */;
INSERT INTO `dashbord` VALUES (1,0,60000,0,10000,60000,3146,93,3,'2022-11-12 00:00:00','2022-12-12 00:00:00',1200,3000),(2,7500,15000,0,2500,22500,3399,109,0,'2022-10-14 00:00:00','2022-11-13 00:00:00',450,1125);
/*!40000 ALTER TABLE `dashbord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deal`
--

DROP TABLE IF EXISTS `deal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `motif` varchar(100) NOT NULL,
  `type_deal` varchar(16) NOT NULL,
  `payment_way` varchar(16) DEFAULT NULL,
  `devise` varchar(16) DEFAULT NULL,
  `amount` int(11) NOT NULL,
  `friend_accept` tinyint(1) NOT NULL,
  `friend_reject` tinyint(1) NOT NULL,
  `payment_bill` varchar(500) DEFAULT NULL,
  `bill_is_added` tinyint(1) NOT NULL,
  `admin_confirm_bill` tinyint(1) NOT NULL,
  `work_did` varchar(500) DEFAULT NULL,
  `work_valid` varchar(500) DEFAULT NULL,
  `work_score` int(11) DEFAULT NULL,
  `deal_over` tinyint(1) NOT NULL,
  `deal_over_time` datetime DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `friend_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `friend_id` (`friend_id`),
  KEY `ix_deal_deal_over_time` (`deal_over_time`),
  KEY `ix_deal_motif` (`motif`),
  KEY `ix_deal_timestamp` (`timestamp`),
  CONSTRAINT `deal_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `deal_ibfk_2` FOREIGN KEY (`friend_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deal`
--

LOCK TABLES `deal` WRITE;
/*!40000 ALTER TABLE `deal` DISABLE KEYS */;
INSERT INTO `deal` VALUES (1,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1663280808.264765sex_m.jpg',1,1,NULL,NULL,1,1,'2022-09-16 02:50:19','2022-09-15 22:14:10',19,2),(2,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1663402494.454547FB_IMG_1654091237175.jpg',1,1,NULL,NULL,3,1,'2022-09-18 11:57:56','2022-09-16 14:32:36',10,2),(3,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1663485943.474555Recu_de_versement.jpg',1,1,NULL,NULL,3,1,'2022-09-18 12:09:43','2022-09-16 17:20:11',4,2),(4,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1663396103.580014307017927_1520348001758345_3295238855571726463_n.jpg',1,1,NULL,NULL,3,1,'2022-09-17 16:39:57','2022-09-17 06:24:23',8,2),(6,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1664175102.54752820220925_101241.jpg',1,1,NULL,NULL,1,1,'2022-09-26 07:59:10','2022-09-23 21:44:16',27,2),(7,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1664183071.298983Screenshot_20220925-201015_Gallery-min.jpg',1,1,NULL,NULL,1,1,'2022-09-27 01:26:07','2022-09-25 16:30:10',18,2),(8,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1664663429.5315recut-de-payment-300x159.png',1,1,NULL,NULL,3,1,'2022-10-01 22:38:12','2022-09-28 12:35:06',5,2),(9,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1664388186.666135bill.jpeg',1,1,NULL,NULL,3,1,'2022-09-28 18:05:43','2022-09-28 18:01:52',12,2),(10,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1664962009.95955820220927_1340051.jpg',1,1,NULL,NULL,1,1,'2022-10-05 10:35:00','2022-10-04 17:21:37',36,2),(11,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1665263765.176725recu_fake_pour_ne_pas_avoir_trouve_lancien.PNG',1,1,NULL,NULL,1,1,'2022-10-08 23:58:28','2022-10-08 20:52:35',9,2),(12,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1665464629.974967recu_fake_pour_ne_pas_avoir_trouve_lancien.PNG',1,1,NULL,NULL,1,1,'2022-10-11 05:11:34','2022-10-08 21:58:32',24,2),(13,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1665469756.82888120220925_134537-min3112.jpg',1,1,NULL,NULL,1,1,'2022-10-12 23:12:16','2022-10-11 05:42:32',22,2),(14,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1669127664.566388recut-de-payment-300x159.png',1,1,NULL,NULL,1,1,'2022-11-22 14:41:29','2022-10-15 17:55:53',49,2),(15,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1667748879.765111Recu_de_paiement_page-0001.jpg',1,1,NULL,NULL,1,1,'2022-11-06 16:02:26','2022-11-05 16:49:36',52,2),(16,'Souscription à l\'offre standard','abon','cash','DA',7500,1,0,'assets/images/bill_img/1667910839.70458716679107143936619381336901289670.jpg',1,1,NULL,NULL,5,1,'2022-11-08 12:40:50','2022-11-08 11:56:04',53,1),(17,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1668245957.260976ca.jpg',1,1,NULL,NULL,3,1,'2022-11-12 09:48:39','2022-11-12 09:32:37',26,2),(18,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1668276561.989445Recu_de_paiment_-_Monsef.jpg',1,1,NULL,NULL,1,1,'2022-11-13 21:46:46','2022-11-12 12:46:08',23,2),(19,'Paiement de caution annuelle de traducteur','test','cash','DA',15000,1,0,'assets/images/bill_img/1669141747.161214USER_SCOPED_TEMP_DATA_orca-image-2042732139.jpeg',1,1,NULL,NULL,1,1,'2022-11-22 22:48:57','2022-11-20 19:59:46',56,2);
/*!40000 ALTER TABLE `deal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `newsletter`
--

DROP TABLE IF EXISTS `newsletter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `newsletter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_newsletter_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `newsletter`
--

LOCK TABLES `newsletter` WRITE;
/*!40000 ALTER TABLE `newsletter` DISABLE KEYS */;
INSERT INTO `newsletter` VALUES (1,'hoodaboukhris@gmail.com','2022-09-15 18:15:26'),(2,'belkada.chabha@yahoo.fr','2022-09-17 16:46:17'),(3,'','2022-09-18 07:29:07'),(4,'kaouthar.alikhodja@yahoo.com','2022-09-18 11:55:54'),(5,'alvinebikele@gmail.com','2022-10-06 16:24:45'),(6,'hanameriem@yahoo.fr','2022-10-13 08:37:55'),(7,'entreprise_safi2010@yahoo.fr','2022-10-13 11:46:06'),(8,'tradrdv.com@buycodeshop.com','2022-12-04 09:56:16');
/*!40000 ALTER TABLE `newsletter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `motif` varchar(100) NOT NULL,
  `amount` int(11) NOT NULL,
  `devise` varchar(16) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_payment_motif` (`motif`),
  KEY `ix_payment_timestamp` (`timestamp`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (1,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-09-15 22:46:11',19),(2,'Paiement de caution annuelle de traducteur',2500,'DA','2022-09-16 02:50:19',2),(3,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-09-17 06:32:05',8),(4,'Paiement de caution annuelle de traducteur',2500,'DA','2022-09-17 16:39:57',2),(5,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-09-18 11:54:27',10),(6,'Paiement de caution annuelle de traducteur',2500,'DA','2022-09-18 11:57:56',2),(7,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-09-18 11:59:56',4),(8,'Paiement de caution annuelle de traducteur',2500,'DA','2022-09-18 12:09:43',2),(9,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-09-26 07:34:49',27),(10,'Paiement de caution annuelle de traducteur',2500,'DA','2022-09-26 07:59:11',2),(11,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-09-27 01:05:59',18),(12,'Paiement de caution annuelle de traducteur',2500,'DA','2022-09-27 01:26:07',2),(13,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-09-28 18:04:27',12),(14,'Paiement de caution annuelle de traducteur',2500,'DA','2022-09-28 18:05:43',2),(15,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-10-01 22:35:21',5),(16,'Paiement de caution annuelle de traducteur',2500,'DA','2022-10-01 22:38:12',2),(17,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-10-05 10:16:12',36),(18,'Paiement de caution annuelle de traducteur',2500,'DA','2022-10-05 10:35:00',2),(19,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-10-08 23:35:19',9),(20,'Paiement de caution annuelle de traducteur',2500,'DA','2022-10-08 23:58:28',2),(21,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-10-11 05:04:29',24),(22,'Paiement de caution annuelle de traducteur',2500,'DA','2022-10-11 05:11:34',2),(23,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-10-12 23:06:52',22),(24,'Paiement de caution annuelle de traducteur',2500,'DA','2022-10-12 23:12:16',2),(25,'60000',0,'DA','2022-10-21 06:54:25',3),(26,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-11-06 15:47:58',52),(27,'Paiement de caution annuelle de traducteur',2500,'DA','2022-11-06 16:02:26',2),(28,'Souscription à l\'offre standard',-7500,'DA','2022-11-08 12:40:50',53),(29,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-11-12 09:45:38',26),(30,'Paiement de caution annuelle de traducteur',2500,'DA','2022-11-12 09:48:39',2),(31,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-11-13 21:44:43',23),(32,'Paiement de caution annuelle de traducteur',2500,'DA','2022-11-13 21:46:46',2),(33,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-11-22 14:40:08',49),(34,'Paiement de caution annuelle de traducteur',2500,'DA','2022-11-22 14:41:29',2),(35,'Paiement de caution annuelle de traducteur',-15000,'DA','2022-11-22 22:45:56',56),(36,'Paiement de caution annuelle de traducteur',2500,'DA','2022-11-22 22:48:57',2);
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `traducteur`
--

DROP TABLE IF EXISTS `traducteur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `traducteur` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dispo` tinyint(1) NOT NULL,
  `accept_subscriber` tinyint(1) NOT NULL,
  `CCP_number` varchar(64) DEFAULT NULL,
  `BaridiMob_RIP` varchar(64) DEFAULT NULL,
  `ePayment_type` varchar(32) DEFAULT NULL,
  `ePayment` varchar(64) DEFAULT NULL,
  `id_card` varchar(500) DEFAULT NULL,
  `diploma` varchar(500) DEFAULT NULL,
  `about_me` varchar(500) DEFAULT NULL,
  `prestation` varchar(32) NOT NULL,
  `phone` varchar(32) NOT NULL,
  `addr_postale` varchar(64) NOT NULL,
  `caution_annual_begin` datetime DEFAULT NULL,
  `caution_annual_end` datetime DEFAULT NULL,
  `remain_day` int(11) DEFAULT NULL,
  `test_score` int(11) NOT NULL,
  `success_work` int(11) NOT NULL,
  `unsuccess_work` int(11) NOT NULL,
  `skill_1` varchar(64) NOT NULL,
  `skill_2` varchar(64) DEFAULT NULL,
  `skill_3` varchar(64) DEFAULT NULL,
  `skill_4` varchar(64) DEFAULT NULL,
  `skill_5` varchar(64) DEFAULT NULL,
  `skill_6` varchar(64) DEFAULT NULL,
  `skill_7` varchar(64) DEFAULT NULL,
  `skill_8` varchar(64) DEFAULT NULL,
  `skill_9` varchar(64) DEFAULT NULL,
  `skill_10` varchar(64) DEFAULT NULL,
  `current_country` varchar(32) DEFAULT NULL,
  `current_town` varchar(32) DEFAULT NULL,
  `compte_valid` tinyint(1) NOT NULL,
  `need_help_ad` varchar(16) DEFAULT NULL,
  `profile_view` int(11) NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `prestation_2` varchar(32) DEFAULT NULL,
  `prestation_3` varchar(32) DEFAULT NULL,
  `prestation_4` varchar(32) DEFAULT NULL,
  `prestation_5` varchar(32) DEFAULT NULL,
  `prestation_6` varchar(32) DEFAULT NULL,
  `prestation_7` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_traducteur_current_country` (`current_country`),
  KEY `ix_traducteur_timestamp` (`timestamp`),
  CONSTRAINT `traducteur_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `traducteur`
--

LOCK TABLES `traducteur` WRITE;
/*!40000 ALTER TABLE `traducteur` DISABLE KEYS */;
INSERT INTO `traducteur` VALUES (1,1,1,NULL,NULL,NULL,NULL,'assets/images/dev/88591.png','assets/images/dev/diploma.pdf','Je suis traductrice professionnelle depuis plus de 5ans maintemant, je suis à votre dispotion. Engagez moi!','Traduction','+213 658489196','42000, Tipasa, Algérie','2022-09-14 20:51:58','2023-09-14 20:51:58',280,5,17,0,'Arabe-français','Arabe-anglais','','','','','','','','','Algérie (arabe)','Tipaza',1,'off',78,'2022-09-14 20:51:58',2,NULL,NULL,NULL,NULL,NULL,NULL),(2,1,1,'00799999002693554794','','','','assets/images/dev/88591.png','assets/images/dev/diploma.pdf','                            Je suis traducteur chez TRADRDV\r\n                        ','Traduction','0792916791','09000','2022-09-16 02:50:19','2023-09-16 02:50:19',364,3,0,0,'Français–anglais','Français–chinois','Arabe-ukrainien','','','','','','','','Algérie (arabe)','Blida',0,'off',7,'2022-09-15 22:14:10',19,NULL,NULL,NULL,NULL,NULL,NULL),(3,1,1,'180415841','00799999000180415841','Payonner','titahyazid@gmail.com','assets/images/dev/88591.png','assets/images/dev/diploma.pdf','                            Experienced professional translator and proofreader.\r\n                        ','Traduction','+213550262029','16061','2022-09-18 11:57:56','2023-09-18 11:57:56',284,3,0,0,'Tamazight-anglais','Tamazight-Français','Français–anglais','Anglais–français','Arabe-anglais','Anglais–arabe','Arabe-français','Français–arabe','Français–tamazight','Anglais–tamazight','Algérie (arabe)','Alger',1,'off',106,'2022-09-16 14:32:36',10,'','','','','',''),(4,1,1,'GHEDIRI Hanane -  0002054044 clé 96 - adresse : Tipaza','00799999000205404496','Payonner','hananeinterpretingworld@gmail.com ','assets/images/dev/88591.png','assets/images/dev/diploma.pdf','                            Diplômée depuis 2022, je maîtrise parfaitement mes combinaisons de prestation.\r\n                        ','Interprétation','00213658489196','42000','2022-09-18 12:09:43','2023-09-18 12:09:43',284,3,0,0,'Arabe-français','Arabe-anglais','Français–arabe','Français–anglais','Anglais–arabe','Anglais–français','','','','','Algérie (arabe)','Tipaza',1,'off',81,'2022-09-16 17:20:11',4,'','','','','',''),(5,1,1,'Mme Bensaddek Lynda 0023206367 42',NULL,NULL,NULL,'assets/images/id_card_img/IMG_0037.jpg','assets/images/diploma_file/CamScanner%2009-06-2022%2009.19.pdf','Je suis une traductrice très sérieuse et dynamique avec beaucoup d\'expérience','Traduction','0792916791','22000, 39 Houaria Abdeljader','2022-09-17 00:33:33','2023-09-17 05:56:55',283,3,0,0,'Arabe-français','Arabe-anglais','Français–anglais','Français–arabe','Anglais–arabe','Anglais–français','','','','','Algérie (arabe)','Sidi Bel Abbès',1,'off',81,'2022-09-17 00:33:33',3,'Interprétation','','','','',''),(6,1,1,'0006623008 clé 80 ','','','','assets/images/dev/88591.png','assets/images/dev/diploma.pdf','Je suis un traducteur très sérieuse et dynamique avec beaucoup d\'expérience','Traduction','0792916791','09000, Tizi ouzou','2022-09-17 16:39:57','2023-09-17 16:39:57',283,3,0,0,'Arabe-allemand','Arabe-français','Français–arabe','Allemand–français','Allemand–arabe','Français–allemand','','','','','Algérie (arabe)','Tizi Ouzou',1,'off',75,'2022-09-17 06:24:23',8,'Interprétation','','','','',''),(8,1,1,'0010169150/32','00799999001016915032','Compte Bancaire','0087601319320100133','assets/images/id_card_img/1663969455.734274CamScanner_09-23-2022_22.27_2.jpg','assets/images/diploma_file/1663969456.137496CamScanner_09-23-2022_22.27_1.jpg','                            Une traductrice sérieuse et dynamique.\r\n                        ','Traduction','0779891131','48004. Ammi Moussa','2022-09-26 07:59:10','2023-09-26 07:59:10',292,3,0,0,'Français–arabe','Arabe-anglais','','','','Anglais–arabe','Arabe-français','Français–anglais','','','Algérie (arabe)','Relizane',1,'off',68,'2022-09-23 21:44:16',27,'Relecture','Transcription','Sous-titrage','','',''),(9,1,1,'0019830172 81','','','','assets/images/id_card_img/1664123409.51947920220925_172517.jpg','assets/images/diploma_file/1664123409.813028Screenshot_20220925-172541_Samsung_Notes.jpg','                            Bonjour,\r\nSi vous avez besoin d\'une personne pour traduire vos documents, n\'hésitez pas à me contacter. \r\n                        ','Traduction','0561092023','42000','2022-09-27 01:26:07','2023-09-27 01:26:07',293,3,0,0,'Arabe-français','Français–anglais','Arabe-anglais','','','','','','','','Algérie (arabe)','Tipaza',1,'off',52,'2022-09-25 16:30:10',18,'Transcription','Interprétation','Sous-titrage','Sous-titrage','',''),(10,1,1,'8570533/38','','','','assets/images/id_card_img/1664368505.496611DIPLOME.jpg','assets/images/diploma_file/1664368505.893636CNI.jpg','Pour moi les langues c\'est un goût et une vocation.\r\nJe les interprète comme une ouverture sur le monde et le meilleur moyen de connaître d\'autres cultures...\r\n\r\n                        ','Traduction','+213 770685855','27000 Coop. Nassim El Bahr  Zaghloul A/02/14','2022-10-01 22:38:12','2023-10-01 22:38:12',297,3,0,0,'Arabe-français','Espagnol-français','','','','Arabe-espagnol','Français–espagnol','','','','Algérie (arabe)','Mostaganem',1,'off',66,'2022-09-28 12:35:06',5,'Transcription','Relecture','Sous-titrage','Interprétation','Voix-off',''),(11,1,1,'1900473 Clé 62','','','','assets/images/id_card_img/1664388111.843378card_id.PNG','assets/images/diploma_file/1664388112.245587dipl.pdf','                            Traductrice avec expérience en relecture, correction et transcription dans les domaines de Droit, Finances, Marketing et Littérature \r\n                        ','Traduction','+213540817343','16004','2022-09-28 18:05:43','2023-09-28 18:05:43',294,3,0,0,'Arabe-français','Anglais–français','Français–arabe','','','','','','','','Algérie (arabe)','Alger',1,'off',62,'2022-09-28 18:01:52',12,'Relecture','Transcription','','','',''),(12,1,1,'','','Western Union','veuillez introduire votre compte bancaire + votre Payoneer ','assets/images/id_card_img/1664904096.565154ID_Card_BIKELE.jpg','assets/images/diploma_file/1664904097.053945DIPLOMES_BIKELE.pdf','                             Passionnée des langues, mes études supérieures m\'ont tout d\'abord ouvert les portes de l\'enseignement, puis par reconversion celles de la traduction En - De - Fr.\r\n                        ','Traduction','00237 699 61 87 13','3&426, rue de Nsimeyong, 111','2022-10-05 10:35:00','2023-10-05 10:35:00',301,3,0,0,'Anglais–français','Allemand–français','Français–allemand','Anglais–allemand','Allemand–anglais','','','','','','Cameroun (français-anglais)','Yaoundé',1,'off',56,'2022-10-04 17:21:37',36,'Relecture','Transcription','Sous-titrage','','',''),(13,1,1,'007999990012379265 clé 25','','','','assets/images/id_card_img/1665262354.9278181664100791624.jpg','assets/images/diploma_file/1665262355.226529Diplome_Licence_Soltani.pdf','                            J\'ai une carrière de 5 ans dans l\'enseignement comme professeur de français, possédant aussi une excellente maîtrise de la langue anglaise...\r\n                        ','Traduction','+213 674304816','12000','2022-10-08 23:58:28','2023-10-08 23:58:28',304,3,0,0,'Français–arabe','Arabe-français','Anglais–arabe','Arabe-anglais','Français–anglais','Anglais–français','','','','','Algérie (arabe)','Tébessa',1,'off',64,'2022-10-08 20:52:35',9,'Transcription','Relecture','Sous-titrage','','',''),(14,1,1,'','00799999001986329928','Payonner','sha.toubaline@gmail.com','assets/images/id_card_img/1665266311.442228Passeport-min.jpg','assets/images/diploma_file/1665266312.091068Diplome_master_2_compressed.pdf','                            Expérience en relecture, correction et traduction, n\'hésitez pas à me contacter.\r\n                        ','Traduction','+213552395417','16006','2022-10-11 05:11:34','2023-10-11 05:11:34',307,3,0,0,'Français–anglais','Anglais–français','','','','','','','','','Algérie (arabe)','Alger',1,'off',40,'2022-10-08 21:58:32',24,'Relecture','','','','',''),(15,1,1,'7855686 clé 17','','','','assets/images/id_card_img/1665466951.02766920220925_140534-min1.jpg','assets/images/diploma_file/1665466951.7425720220925_131502-1.pdf','                            Passionnée de culture, de tourisme, et d\'histoire, avec une excellente culture générale, j\'ai aussi une expérience pro. dans les relations internationales.\r\n                        ','Traduction','+213 662133025','Bir Mourad Rais','2022-10-12 23:12:16','2023-10-12 23:12:16',308,3,0,0,'Arabe-français','Français–arabe','','','','Anglais–français','','','','','Algérie (arabe)','Alger',1,'off',43,'2022-10-11 05:42:32',22,'Relecture','','','','',''),(16,1,1,'','','','','assets/images/id_card_img/1665856551.96131620221015_184819.jpg','assets/images/diploma_file/1665856552.514364IMG_20221012_131333.pdf','                            Bonjour, Je rédige tout type de contenus en français, j\'effectue des corrections ainsi que des relectures de supports variés. Je propose également des services de traduction, de l\'arabe vers le français et vice versa.\r\n                        ','Traduction','+213669819478','43001','2022-11-22 14:41:29','2023-11-22 14:41:29',349,1,0,0,'Arabe-français','Français–arabe','','','','','','','','','Algérie (arabe)','Mila',1,'off',25,'2022-10-15 17:55:53',49,'Relecture','Sous-titrage','','','',''),(17,1,1,'728998','00799999000072899877','','','assets/images/id_card_img/1667666975.889377010.jpg','assets/images/diploma_file/1667666976.139619diplome_master.pdf','                            dynamique,comprehensif,en faisant du bon travaitdans les meilleurs délaits.\r\n                        ','Traduction','+2130773222690','05028-barika.benbatouche','2022-11-06 16:02:26','2023-11-06 16:02:26',333,3,0,0,'Français–arabe','Français–anglais','Arabe-français','Arabe-anglais','Anglais–arabe','Arabe-anglais','','','','','Algérie (arabe)','Batna',1,'off',44,'2022-11-05 16:49:36',52,'Traduction','Interprétation','Relecture','Sous-titrage','Interprétation','Traduction'),(18,1,1,'','0079999900080941 93','','','assets/images/id_card_img/1668245556.229333Capture_111.jpg','assets/images/diploma_file/1668245556.467351Diplome_compressed_compressed.pdf','                            Jeune femme traductrice, passionnée de langues étrangères, ambitionne de percer dans ce domaine et de donner le maximum pour cette plateforme.\r\n                        ','Traduction','0000000000','Cité Ennassim 136 logts Chaareddib Abdelmadjid N°03 ','2022-11-12 09:48:39','2023-11-12 09:48:39',339,3,0,0,'Français–anglais','Anglais–français','Français–arabe','Arabe-français','Arabe-anglais','Anglais–arabe','','','','','Algérie (arabe)','Constantine',1,'off',27,'2022-11-12 09:32:37',26,'Relecture','Transcription','Voix-off','','',''),(19,1,1,'0023654248  ','','Payonner','monsefoualaeddine@gmail.com','assets/images/id_card_img/1668257167.71028Passport_Monsef_page-0001.jpg','assets/images/diploma_file/1668257168.041853BA_Degree.pdf','                             I specialize in TRANSLATION, PROOFREADING, LOCALIZATION \r\nFrom and into English, French and Arabic.\r\n\r\nI always make sure to provide well done, accurate translations which ensure that nothing gets lost in there. All hassle-free, and in a delightfully timely manner!\r\n                        ','Traduction','0549158888','Ain Oulmene','2022-11-13 21:46:46','2023-11-13 21:46:46',340,1,0,0,'Arabe-anglais','Arabe-français','Français–anglais','','','Anglais–arabe','Français–arabe','Anglais–français','','','Algérie (arabe)','Sétif',1,'off',18,'2022-11-12 12:46:08',23,'Sous-titrage','Transcription','Interprétation','','',''),(20,1,1,'0020611309 clé 93','','PayPal','ridha mohammedi','assets/images/id_card_img/1668974385.746375carte_national.jpg','assets/images/diploma_file/1668974386.06173diplome_master_1.pdf','                            traducteur, journaliste, prof des langues étrangères, très sérieux, admirateur du perfection.\r\n                        ','Traduction','00213667323875/00213542044734','02000','2022-11-22 22:48:57','2023-11-22 22:48:57',349,1,0,0,'Arabe-français','Français–arabe','Arabe-anglais','Anglais–arabe','','','','','','','Algérie (arabe)','Chlef',1,'off',15,'2022-11-20 19:59:46',56,'Traduction','Traduction','Traduction','Traduction','Interprétation','Interprétation');
/*!40000 ALTER TABLE `traducteur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pseudo_com` varchar(32) DEFAULT NULL,
  `username` varchar(32) DEFAULT NULL,
  `fullname` varchar(64) DEFAULT NULL,
  `sex` varchar(16) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `statut` varchar(16) DEFAULT NULL,
  `ad_statut` tinyint(1) NOT NULL,
  `offre_statut` varchar(16) DEFAULT NULL,
  `offre_begin` datetime DEFAULT NULL,
  `offre_end` datetime DEFAULT NULL,
  `daily_offer` int(11) DEFAULT NULL,
  `remain_day` int(11) DEFAULT NULL,
  `avatar` varchar(500) DEFAULT NULL,
  `country` varchar(32) DEFAULT NULL,
  `revenu` int(11) NOT NULL,
  `confirmed` tinyint(1) DEFAULT NULL,
  `google_login` tinyint(1) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL,
  `link_com` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_email` (`email`),
  UNIQUE KEY `ix_user_username` (`username`),
  KEY `ix_user_pseudo_com` (`pseudo_com`),
  KEY `ix_user_timestamp` (`timestamp`),
  KEY `ix_user_sex` (`sex`),
  KEY `ix_user_country` (`country`),
  KEY `ix_user_fullname` (`fullname`),
  KEY `ix_user_link_com` (`link_com`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,NULL,'Hanane_A','Hanane GHEDIRI','Féminin','tradrdv.panel@gmail.com','pbkdf2:sha256:260000$glKmv1epd4tkwTNl$0c5e6fba1cc6a49f53642ccfc0482a38ba071c26e253e95161c2765289c8816d','admin',0,'gratuit','2022-09-14 20:51:58','2022-09-14 20:51:58',1,0,'assets/images/dev/sex_f.jpg','Algérie (arabe)',0,1,0,'2022-09-14 20:51:58','2022-12-08 15:49:31',''),(2,NULL,'Hanane_T','Hanane GHEDIRI','Féminin','testeurdefaut@gmail.com','pbkdf2:sha256:260000$glKmv1epd4tkwTNl$0c5e6fba1cc6a49f53642ccfc0482a38ba071c26e253e95161c2765289c8816d','testeur',0,'gratuit','2022-09-14 20:51:58','2022-09-14 20:51:58',1,0,'assets/images/dev/sex_f.jpg','Algérie (arabe)',42500,1,0,'2022-09-14 20:51:58','2022-12-01 13:20:45',''),(3,NULL,'Didouche','Bensaddek Lynda','Féminin','bensaddek40@gmail.com','pbkdf2:sha256:260000$SwhVPtMGj4MCXoNJ$659b98b67561c871f3121caed09cdbd782e9b9e7e6b12f1a063861cf272053bb','traducteur',0,'gratuit','2022-09-15 05:44:16','2022-09-15 05:44:16',1,0,'assets/images/dev/sex_f.jpg','Algérie (arabe)',0,1,0,'2022-09-15 05:44:16','2022-11-08 09:05:47',''),(4,NULL,'Abdel','Ghili Abdelkrim','Masculin','abdelkrim.ghili@gmail.com','pbkdf2:sha256:260000$eTMU5XjJAEEFbnNj$e4c5c84a05dd508de5fddae8172a36a4a935453a3b5211b2ab7f6516a06d8c59','traducteur',0,'gratuit','2022-09-15 07:33:26','2022-09-15 07:33:26',1,0,'assets/images/dev/sex_m.jpg','Algérie (arabe)',0,1,0,'2022-09-15 07:33:26','2022-11-10 11:30:25',''),(5,NULL,'Dadin','BENANI Abdelkader ','Masculin','dadin5466@gmail.com','pbkdf2:sha256:260000$XTBAnHFPSwXfhHbi$f6988e74b54a0a9cfcecde80b2aa6de1fc8d1465d61f9c961eeccbd6fdb4b865','traducteur',0,'gratuit','2022-09-15 08:08:06','2022-09-15 08:08:06',1,0,'assets/images/dev/sex_m.jpg','Algérie (arabe)',0,1,0,'2022-09-15 08:08:06','2022-10-23 09:26:14',''),(6,NULL,'tizioualou.sonia@gmail.com','Sonia Tizioualou',NULL,'tizioualou.sonia@gmail.com','pbkdf2:sha256:260000$XYu34sgmqHtv7QPD$a70d037aa15ffbbb4fdb166a58fad63cd10a423e3c9fbe5924c22c5f8ad71dad','client',0,'gratuit','2022-09-15 08:18:32','2022-09-15 08:18:32',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,1,0,'2022-09-15 08:18:32','2022-09-15 08:30:14',''),(7,NULL,'Sara-162','Sara Ait yakoub ',NULL,'aityakoubsara@gmail.com','pbkdf2:sha256:260000$Oad7j1kGjLm0fWov$dec0d2bb44f159a77475b0c92389017d8fa293c536802a632e7cf29ed238cdbb','client',0,'gratuit','2022-09-15 08:43:15','2022-09-15 08:43:15',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,1,0,'2022-09-15 08:43:15','2022-09-15 08:45:35',''),(8,NULL,'Mohand','Mohand  Ouramdane Mehenni ','Masculin','mohand.ouramdane.mehenni@gmail.com','pbkdf2:sha256:260000$TUwNoCgOuGwu7jzh$98184dc7490a0da6cdd7aeb3c4526531d0f6c3e1dd84f108902db2a27b860f02','traducteur',0,'gratuit','2022-09-15 09:12:48','2022-09-15 09:12:48',1,0,'assets/images/dev/sex_m.jpg','Algérie (arabe)',0,1,0,'2022-09-15 09:12:48','2022-10-04 15:16:17',''),(9,NULL,'Franka','SOLTANI Abd Elhamid ','Masculin','solhamid656@gmail.com','pbkdf2:sha256:260000$FWBZQsBoULw5Nf7A$1589888261143ff69a30a2b9193fed8fe4be1367a64c7a0166bf7070fa7c6009','traducteur',0,'gratuit','2022-09-15 09:45:05','2022-09-15 09:45:05',1,0,'assets/images/dev/sex_m.jpg','Algérie (arabe)',0,1,0,'2022-09-15 09:45:05','2022-10-08 23:57:32',''),(10,NULL,'tyazid25','Yazid Titah ','Masculin','tyazid25@gmail.com','pbkdf2:sha256:260000$eF47iSEjCwZslB0o$9f54a8d09a47db860d49e41c345b5c0338399f17208f0826d72451219c2652e5','traducteur',0,'gratuit','2022-09-15 12:22:35','2022-09-15 12:22:35',1,0,'assets/images/dev/sex_m.jpg','Algérie (arabe)',0,1,0,'2022-09-15 12:22:35','2022-12-07 16:42:33',''),(11,NULL,'hooda_nardjes','Houda BOUKHRIS ',NULL,'hoodaboukhris@gmail.com','pbkdf2:sha256:260000$OcBMaOaT2xe1gXtg$1ffef70cff2e47f5f5d342cbb103fd85a559716b4a77b3a1c496c30d8783fdd9','client',0,'gratuit','2022-09-15 12:32:52','2022-09-15 12:32:52',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,1,0,'2022-09-15 12:32:52','2022-09-16 19:59:40',''),(12,NULL,'Selma Abdelwahab','Abdelwahab Selma','Féminin','eurlwmstudies@gmail.com','pbkdf2:sha256:260000$Ep4K6oupf6N5RTlq$f3117c655c993af22e05cebd5ba90065f2e40fb7fafbd3ab9f20cf3e31bab28d','traducteur',0,'gratuit','2022-09-15 13:50:06','2022-09-15 13:50:06',1,0,'assets/images/dev/sex_f.jpg','Algérie (arabe)',0,1,0,'2022-09-15 13:50:06','2022-09-28 18:03:21',''),(13,NULL,'Hadjazi Naila ','Hadjazi Naila ',NULL,'hadjazi.naila23@gmail.com','pbkdf2:sha256:260000$FhC5uSGJCmKDEmvZ$24e4d4a23f6c1f58fa29adb18cf930f1241023ac1b97d5220bfb98cefb517911','client',0,'gratuit','2022-09-15 14:07:32','2022-09-15 14:07:32',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,1,0,'2022-09-15 14:07:32','2022-09-15 14:13:46',''),(14,NULL,'Hafsa','Hafiane Hafsa',NULL,'hafsa0450@gmail.com','pbkdf2:sha256:260000$sZU9FvDqdQD9Tee7$2b6d93ec1a687d0b803003b88c445f1fb6e39d3e83c41e2114b9e947d1204f1d','client',0,'gratuit','2022-09-15 14:30:50','2022-09-15 14:30:50',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,1,0,'2022-09-15 14:30:50','2022-10-10 22:37:24',''),(15,NULL,'Hako1990','Abdelhak','Masculin','abdelhak.sakher@gmail.com','pbkdf2:sha256:260000$TVzRL0FMw25wDNct$410e3c95c53aad5f1f543a4c7c9974b3c1ce4e6092f6601080ef966fccc965bc','client',0,'gratuit','2022-09-15 15:37:44','2022-09-15 15:37:44',1,0,'assets/images/dev/sex_m.jpg','Algérie (arabe)',0,1,1,'2022-09-15 15:37:44','2022-11-09 19:33:09',''),(16,NULL,'S. Hamza ','SAHOUI Hamza ',NULL,'sahoui.h@gmail.com','pbkdf2:sha256:260000$YTmIujndx4FI9VqI$33ac94c0003c68b8d965d59afd0dd2592674c0d5a79d955b1608feecd57b2e02','client',0,'gratuit','2022-09-15 15:51:08','2022-09-15 15:51:08',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,0,0,'2022-09-15 15:51:08','2022-09-15 15:51:08',''),(17,NULL,NULL,'Boubeker Nadia Wafaa ','Féminin','wafaaboubeker@gmail.com','pbkdf2:sha256:260000$1i9PGUidutJc702P$5e174f3f57b28d22336a471aba13d9a78dfa489186484150f6fee891a8f3452c','client',0,'gratuit','2022-09-15 17:53:40','2022-09-15 17:53:40',1,0,'assets/images/dev/sex_f.jpg','Algérie (arabe)',0,1,0,'2022-09-15 17:53:40','2022-09-15 18:21:00',''),(18,NULL,'Sarah S','sarah','Féminin','sarahsilem1@gmail.com','pbkdf2:sha256:260000$LjkhWCTrvZPpctAS$137ea774246da48ae397c99c3c30fd7a8e090ae4b418577a8dad86b481077b83','traducteur',0,'gratuit','2022-09-15 20:18:28','2022-09-15 20:18:28',1,0,'assets/images/dev/sex_f.jpg','Algérie (arabe)',0,1,1,'2022-09-15 20:18:28','2022-10-29 11:20:15',''),(19,NULL,'Yvestack01c','Yves Fidèle AIKOUN','Masculin','yvestack01c@gmail.com','pbkdf2:sha256:260000$TpRXipiLRMOWXBcW$f66cd15c823110fe5fbca05c8b781512fe6037ed6edc30d9ceb5cc993ae22223','traducteur',0,'gratuit','2022-09-15 20:45:51','2022-09-15 20:45:51',1,0,'assets/images/dev/sex_m.jpg','Algérie (arabe)',0,1,0,'2022-09-15 20:45:51','2022-10-22 17:41:00',''),(20,NULL,'Impératrice ','Hanane',NULL,'hananeinterpretingworld@gmail.com','pbkdf2:sha256:260000$oXD0xZjawmmOVdGr$631274af51fbcb2a7de35549e935a616b51ef88a1182d3f785c625c1d5903948','client',0,'gratuit','2022-09-16 12:59:09','2022-09-16 12:59:09',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,1,0,'2022-09-16 12:59:09','2022-09-16 20:29:06',''),(21,NULL,'Bahia','Taleb Bahia',NULL,'talebbh00@gmail.com','pbkdf2:sha256:260000$ykd224x9p3v3SUt9$88c05ed2f88c39ac81a8e0594d8d192e72d009923e71aa9f93fa63e3af686c09','client',0,'gratuit','2022-09-16 19:30:30','2022-09-16 19:30:30',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,0,0,'2022-09-16 19:30:30','2022-09-16 19:31:20',''),(22,NULL,'Hanack','CHERFI Hana ','Féminin','hanameriem@yahoo.fr','pbkdf2:sha256:260000$lno2ONBuNu6sXD3D$e22f964098d38247753b6352b3a542279db5de69f45cf01af5938aae65dc3a06','traducteur',0,'gratuit','2022-09-17 12:48:43','2022-09-17 12:48:43',1,0,'assets/images/dev/sex_f.jpg','Algérie (arabe)',0,1,0,'2022-09-17 12:48:43','2022-12-04 12:01:50',''),(23,NULL,'Monsef','REFFAS Monsef Ouala Eddine','Masculin','monsefoualaeddine@gmail.com','pbkdf2:sha256:260000$Avge6ayJbrxws2Q7$0c3925b4bf566d3c14a2ea46e7a0a559cb66099bc592de5af5b495a82c6a80d3','traducteur',0,'gratuit','2022-09-17 14:21:08','2022-09-17 14:21:08',1,0,'assets/images/dev/sex_m.jpg','Émirats arabes unis (arabe)',0,1,0,'2022-09-17 14:21:08','2022-11-13 21:46:00',''),(24,NULL,'Camxlle','Toubaline Camélia Shahrazed','Féminin','sha.toubaline@gmail.com','pbkdf2:sha256:260000$r4blqbBMppk2GeSL$e0e08319976d4d23bdada580b416be78567a92afb4feffc5e80fa5f3cb185613','traducteur',0,'gratuit','2022-09-17 15:58:38','2022-09-17 15:58:38',1,0,'assets/images/dev/sex_f.jpg','Algérie (arabe)',0,1,0,'2022-09-17 15:58:38','2022-10-11 08:28:25',''),(25,NULL,'belkada.chabha@yahoo.fr','Belkada Chabha',NULL,'belkada.chabha@yahoo.fr','pbkdf2:sha256:260000$xiAt322W2NIAM0UJ$9a4044bbb61fe65c5aa3df9df50e9bebe6d8893e0abf2c3ddce1ab158ba8045a','client',0,'gratuit','2022-09-17 16:44:35','2022-09-17 16:44:35',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,0,0,'2022-09-17 16:44:35','2022-09-17 16:46:18',''),(26,NULL,'kaoutar ','Ali-khodja Kaouthar','Féminin','kaouthar.alikhodja@yahoo.com','pbkdf2:sha256:260000$lbqx9FYqYU4Q6Xpl$3058edece12756ee09ccd07e637c4d39d50bac2ee1d50ee81a27fbe76a55576c','traducteur',0,'gratuit','2022-09-18 11:51:09','2022-09-18 11:51:09',1,0,'assets/images/dev/sex_f.jpg','Algérie (arabe)',0,1,0,'2022-09-18 11:51:09','2022-12-06 07:59:46',''),(27,NULL,'Rihab Larabi','Sifou Nadjet','Féminin','sifoun@ymail.com','pbkdf2:sha256:260000$T3lbR4wagCTwukXk$0fe9826599ad8c70af0806757ee10d5c5bb6aab3785b0039429fb546421cf4e5','traducteur',0,'gratuit','2022-09-19 10:29:18','2022-09-19 10:29:18',1,0,'assets/images/dev/sex_f.jpg','Algérie (arabe)',0,1,0,'2022-09-19 10:29:18','2022-10-05 07:42:25',''),(28,NULL,'WeTraduit','Imad','Masculin','wetraduit@gmail.com','pbkdf2:sha256:260000$wKpUtwVXUtEORVF0$a70ef2c4b7d719616a3e6e5ad3f74da56472e061e7f89943e4115d484530713a','client',0,'gratuit','2022-09-20 10:59:33','2022-09-20 10:59:33',1,0,'assets/images/dev/sex_m.jpg','Algérie (arabe)',0,1,1,'2022-09-20 10:59:33','2022-09-20 11:16:09',''),(29,NULL,'Marc','Programm','Masculin','programm01dev@gmail.com','pbkdf2:sha256:260000$LEUIYZYKzqxTcU3E$c95e6ae79151f54263b4dc21604041f43d59596b0d24c63caf52fde463483cab','traducteur',0,'gratuit','2022-09-21 11:33:18','2022-09-21 11:33:18',1,0,'assets/images/dev/sex_m.jpg','Algérie (arabe)',0,1,1,'2022-09-21 11:33:18','2022-09-21 11:37:58',NULL),(30,NULL,'AesirProject','Mohamed Rechache','Masculin','dzhawke@gmail.com','pbkdf2:sha256:260000$S9jvGLg2zlyK6O1o$116e0ddc5882ba529adc9b61b1d913cd061e10d9ebeb7e6e295a340782fb528a','client',0,'gratuit','2022-09-22 22:12:11','2022-09-22 22:12:11',1,0,'assets/images/dev/sex_m.jpg','Algérie (arabe)',0,1,0,'2022-09-22 22:12:11','2022-10-27 23:01:02',NULL),(31,NULL,'Kahina TABTI ','Kahina TABTI ',NULL,'tabtikahina@yahoo.fr','pbkdf2:sha256:260000$ZEaF7DXRTfQJr0Oa$2235268a3737435a1a9682f1a4ed12ff36b6651b0ea3fc60efa0354cdc75ed42','client',0,'gratuit','2022-09-23 20:08:30','2022-09-23 20:08:30',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,1,0,'2022-09-23 20:08:30','2022-09-24 05:14:36',NULL),(32,NULL,'faridmezaguer@yahoo.fr','Mohamed Mezaguer',NULL,'faridmezaguer@yahoo.fr','pbkdf2:sha256:260000$DdJAGEd564JzSZT2$93d3622c724e771ebb0b5be125932444e588ebfecac8326e9ad8915d07fbf2d2','client',0,'gratuit','2022-09-25 09:55:22','2022-09-25 09:55:22',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,1,0,'2022-09-25 09:55:22','2022-09-25 10:01:47',NULL),(33,NULL,'chems1233','Chalabi Chems Eddine','Masculin','chamschelabi@gmail.com','pbkdf2:sha256:260000$2jVjhJyR5L4U9G6g$f961b7f4e5fa3a71385dbd300553a58b80c57612c349d9d004d81b954d9e8597','client',0,'gratuit','2022-09-25 13:20:10','2022-09-25 13:20:10',1,0,'assets/images/dev/sex_m.jpg','Algérie (arabe)',0,1,0,'2022-09-25 13:20:10','2022-09-25 21:28:47',NULL),(34,NULL,'Hanane Bouziane','bouziane hanane','Féminin','bouzianehanan@gmail.com','pbkdf2:sha256:260000$QuJ67b4yGxz1PyGx$ce0907917739393e0774ea48d38f279872960f950e23235e9ad07ebb1862c6d7','client',0,'gratuit','2022-09-26 07:57:13','2022-09-26 07:57:13',1,0,'assets/images/dev/sex_f.jpg','Algérie (arabe)',0,1,0,'2022-09-26 07:57:13','2022-09-26 08:07:48',NULL),(35,NULL,'Sam','Daemon',NULL,'Samdaemon25@gmail.com','pbkdf2:sha256:260000$vqR0qzX3HhPhHTYL$0eafd34f21cc62619c8334b6a066ec4a128143b1350ec9290d875e0667ed1057','client',0,'gratuit','2022-09-30 09:31:25','2022-09-30 09:31:25',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,1,0,'2022-09-30 09:31:25','2022-09-30 16:12:20',NULL),(36,NULL,'Bikadn','Alvine BIKELE ','Féminin','alvinebikele@gmail.com','pbkdf2:sha256:260000$FOoNnAPG8LkyhtoC$1c5ee17dd95c748c057acc60ecbe67cf4d656be357bb34a99afaa561575483d4','traducteur',0,'gratuit','2022-10-01 01:15:50','2022-10-01 01:15:50',1,0,'assets/images/dev/sex_f.jpg','Cameroun (français-anglais)',0,1,0,'2022-10-01 01:15:50','2022-12-06 22:50:40',NULL),(37,NULL,'BrownEmerald ','Bouadani Cérine','Féminin','bouadanicerine@gmail.com','pbkdf2:sha256:260000$Qcg7EKzJQT39DnYw$0dd5d80fdc021fdd1ca3d01fe57a6b1002129d0c985f105d773028041d10c9a1','client',0,'gratuit','2022-10-02 09:51:44','2022-10-02 09:51:44',1,0,'assets/images/dev/sex_f.jpg','Algérie (arabe)',0,1,0,'2022-10-02 09:51:44','2022-10-02 17:46:19',NULL),(38,NULL,'H.Bouabid','Hafsa Bouabid','Féminin','bouabidhafsamail@gmail.com','pbkdf2:sha256:260000$6jNMaDBtIn3nTouZ$c72fa354d5eb079abdefb862653dff78a8f90946b4dee1cd26a64eb1e537fb10','client',0,'gratuit','2022-10-04 09:55:49','2022-10-04 09:55:49',1,0,'assets/images/dev/sex_f.jpg','Algérie (arabe)',0,1,0,'2022-10-04 09:55:49','2022-10-04 20:47:07',NULL),(39,NULL,'Lagloire','Gloriane Ngonana',NULL,'glorianengonana@gmail.com','pbkdf2:sha256:260000$g53TcqabvJhetATB$d42cb31d8c2c9c4b64f185092f0564b9e034bd0825736facc1c4d45cd594f2d6','client',0,'gratuit','2022-10-04 16:26:36','2022-10-04 16:26:36',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,0,0,'2022-10-04 16:26:36','2022-10-04 16:28:26',NULL),(40,NULL,'Carelle Matawe','Matawe Fotsing Carelle',NULL,'fotsing237@yahoo.com','pbkdf2:sha256:260000$FcxVZvugy0kxZjHj$509205e3725dce221e795e9abe09a442e5781ec735331f50f206cb4031af5c36','client',0,'gratuit','2022-10-06 21:56:04','2022-10-06 21:56:04',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,0,0,'2022-10-06 21:56:04','2022-10-06 21:56:04',NULL),(42,NULL,'Carelle Fotsing','Matawe Fotsing Carelle','Féminin','mafoca@yahoo.com','pbkdf2:sha256:260000$S0jvykeYKDU9hcU9$64084edd2d2fd3cf6b0744e5a6dd8bb427153d16da31a6d38dcba8c456fd5e13','client',0,'gratuit','2022-10-06 21:56:58','2022-10-06 21:56:58',1,0,'assets/images/dev/sex_f.jpg','Cameroun (français-anglais)',0,1,0,'2022-10-06 21:56:58','2022-10-06 22:01:33',NULL),(43,NULL,'Claire','Chiara Borelli',NULL,'chiara.traduzione1@gmail.com','pbkdf2:sha256:260000$sJfctsKEjmllJBAS$22457c0b83f2abdec24b903be86dc6c6f207ec5cbb99a7f546aa1d62bb7fc279','client',0,'gratuit','2022-10-07 10:18:40','2022-10-07 10:18:40',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,1,0,'2022-10-07 10:18:40','2022-10-07 10:21:02',NULL),(44,NULL,'Wafaa','Nadia Wafaa','Féminin','wafaaboubeker2@gmail.com','pbkdf2:sha256:260000$CRl2p1k6yCrtJoTP$7d07881332add6ade4f2f539ecc89b86542a8c50562724b98d43d20796871676','client',0,'gratuit','2022-10-08 00:47:01','2022-10-08 00:47:01',1,0,'assets/images/dev/sex_f.jpg','Algérie (arabe)',0,1,1,'2022-10-08 00:47:01','2022-10-09 10:51:33',NULL),(45,NULL,'Xzibit ','Houmsia Hamsou Dieudonné ',NULL,'humsha07@hotmail.co.uk','pbkdf2:sha256:260000$fczasfhwUNbCHN0w$930e56526ebd870f9fe794d6cf62bc462859e0fd5d8f9ea64b389cae3d6c159a','client',0,'gratuit','2022-10-09 17:58:36','2022-10-09 17:58:36',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,0,0,'2022-10-09 17:58:36','2022-10-09 18:09:16',NULL),(46,NULL,'Belmabdi','Mohammed Fatah BELMABDI','Masculin','mohammed.f.belmabdi@gmail.com','pbkdf2:sha256:260000$2GTy3wrWQqxu13QF$3392ab581d2d6282d78425a2dd92d4aebdcc5e47ea5c93ade1f048cc02e1df20','client',0,'gratuit','2022-10-09 18:18:12','2022-10-09 18:18:12',1,0,'assets/images/dev/sex_m.jpg','Algérie (arabe)',0,1,0,'2022-10-09 18:18:12','2022-10-09 18:41:29',NULL),(47,NULL,'chaouki','Kamel Chawki ZEGGAR',NULL,'zeggark@gmail.com','pbkdf2:sha256:260000$mN4UyH9rJdw8Coir$83a7411b845226fa0c1e6276c39011d68b822e8c7e150e0682d44a0e68dd24ba','client',0,'gratuit','2022-10-10 08:38:05','2022-10-10 08:38:05',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,0,0,'2022-10-10 08:38:05','2022-10-10 08:38:17',NULL),(48,NULL,'Meriem ','Meriem ikrame ',NULL,'Ikramemeriem@gmail.com','pbkdf2:sha256:260000$vhoL16dsG9aLXkxp$6d06e2f0e8151766e55d0351db5c3a7ae2f96257d956cccbb231974bb9e96f2c','client',0,'gratuit','2022-10-10 10:14:32','2022-10-10 10:14:32',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,0,0,'2022-10-10 10:14:32','2022-10-10 10:15:09',NULL),(49,NULL,'madamekb','Laachi Fatiha','Féminin','pjane3201@gmail.com','pbkdf2:sha256:260000$xFeprhy6DOJeyrcG$1a110c2c9570f4187bc3309bf7ad41251498f3331526b5413fde7f4b2972d266','traducteur',0,'gratuit','2022-10-12 11:38:20','2022-10-12 11:38:20',1,0,'assets/images/dev/sex_f.jpg','Algérie (arabe)',0,1,0,'2022-10-12 11:38:20','2022-12-01 14:53:57',NULL),(50,NULL,'SlimaneBekkaye','Slimane Bekkaye','Masculin','sli.bekkaye@gmail.com','pbkdf2:sha256:260000$KbNTX1Jmz2qwZY6Y$985091cd0125767065e1a181aefedd3202616065eef39fe410586958f4710c4e','client',0,'gratuit','2022-10-15 21:05:32','2022-10-15 21:05:32',1,0,'assets/images/dev/sex_m.jpg','Algérie (arabe)',0,1,0,'2022-10-15 21:05:32','2022-10-16 07:06:15',NULL),(51,NULL,'kayip','Kayip Adam','Masculin','f.kayipadam@gmail.com','pbkdf2:sha256:260000$8bhLLQLI25PYuKIo$ce0b00399aea18dbb5ed7f2751fb74e38c76a3c2c9d3f6de27f5bd22393dc5be','client',0,'gratuit','2022-10-23 07:39:20','2022-10-23 07:39:20',1,0,'assets/images/dev/sex_m.jpg','Turquie (turc)',0,1,0,'2022-10-23 07:39:20','2022-10-23 23:00:02',NULL),(52,NULL,'ahmed','kebabi ahmed','Masculin','kalmi.mohammed@gmail.com','pbkdf2:sha256:260000$N0EhsdJsFjtI0YxN$a3337477e965d91da8e0f050ef938692179d4b09659284effe2b6f21f6dc92c7','traducteur',0,'gratuit','2022-11-05 14:04:48','2022-11-05 14:04:48',1,0,'assets/images/dev/sex_m.jpg','Algérie (arabe)',0,1,0,'2022-11-05 14:04:48','2022-12-01 09:41:16',NULL),(53,NULL,'Pretty soumi','Soumia TAHRI','Féminin','tahri.soumia1983@gmail.com','pbkdf2:sha256:260000$AvfEOEYISjD7Gb3p$52cac89a4633dc5560bc541edf5a9785f95a52a97d68219b816fd215c4d41302','client',0,'standard','2022-11-08 12:40:50','2023-05-09 12:40:50',1,152,'assets/images/dev/sex_f.jpg','Algérie (arabe)',0,1,0,'2022-11-05 23:40:45','2022-12-05 12:12:15',NULL),(54,NULL,'Sofized ','Sofi zed','Masculin','medjrassofiane@yahoo.fr','pbkdf2:sha256:260000$kq3cw7mS2VmJ7Zn8$b119b34ce17fd1320889c54e202544538275f3860e0f6ef12b1868605f971a5a','client',0,'gratuit','2022-11-06 16:13:59','2022-11-06 16:13:59',1,0,'assets/images/dev/sex_m.jpg','Algérie (arabe)',0,1,0,'2022-11-06 16:13:59','2022-11-06 16:22:33',NULL),(55,NULL,'Katia ',' Djaroun Katia ',NULL,'djarounkatia@gmail.com','pbkdf2:sha256:260000$rJNT6WF85nRywRQb$82b042ebdce7f1ae287660ab3303eaa0c0c909701bc2ebdc9818da4b13af4598','client',0,'gratuit','2022-11-12 08:36:17','2022-11-12 08:36:17',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,0,0,'2022-11-12 08:36:17','2022-11-12 08:36:17',NULL),(56,NULL,'Ridhamohammedi','Mohammedi ridha','Masculin','Redapatrik@gmail.com','pbkdf2:sha256:260000$RsMbfHQEly7eQpKN$9eed4d019dcff62f4b0674c1d8694e861f67c718fced5341efd28abc6be7e15b','traducteur',0,'gratuit','2022-11-13 19:57:02','2022-11-13 19:57:02',1,0,'assets/images/dev/sex_m.jpg','Algérie (arabe)',0,1,0,'2022-11-13 19:57:02','2022-11-23 09:27:20',NULL),(57,NULL,'Hakim','Safar Bouni Abdelhakim',NULL,'safarbouni199400@gmail.com','pbkdf2:sha256:260000$217lSYQDQUtpgTlz$b3624ca06e1d0f5ae3e9c5968220f59b206fa940810fcb02ae0e02d30055c6e8','client',0,'gratuit','2022-11-24 21:16:22','2022-11-24 21:16:22',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,0,0,'2022-11-24 21:16:22','2022-11-30 08:35:32',NULL),(58,NULL,'Soumia MAHLIA','Soumia MAHLIA',NULL,'soumiamahlia@gmail.com','pbkdf2:sha256:260000$ACUAZslh3Et694bN$c68faa2ac3dad3d0456cce0a469e40a585045dbdf0891aa27ca85d6104b36c3f','client',0,'gratuit','2022-11-28 11:30:15','2022-11-28 11:30:15',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,0,0,'2022-11-28 11:30:15','2022-11-28 12:47:51',NULL),(59,NULL,'Karima ','Chaibi karima',NULL,'chaibikarima.3191@gmail.com','pbkdf2:sha256:260000$tRbUviLX6CVjOxxH$1cca1d0f1b5a248fbac4a86c0d303123bc4ae7af11417ac1607a1b0e51624cff','client',0,'gratuit','2022-12-01 10:15:36','2022-12-01 10:15:36',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,0,0,'2022-12-01 10:15:36','2022-12-03 20:31:07',NULL),(60,NULL,'Mouna ','Da',NULL,'daili.mouna@yahoo.com','pbkdf2:sha256:260000$mxPUFHpheGrKtTgV$d1057529652e8bafebf6a076304fad99fe5647d4ed41d247d491ae3a3822773e','client',0,'gratuit','2022-12-01 11:30:24','2022-12-01 11:30:24',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,0,0,'2022-12-01 11:30:24','2022-12-01 11:32:57',NULL),(61,NULL,'Titri','Nadjet titri',NULL,'nadjet.titri@outlook.fr','pbkdf2:sha256:260000$r7qBqaxDas8Hz86X$0da16d81393117cf87daa2a54535492f5297fdb03c5a20febeda24deb1c5a006','client',0,'gratuit','2022-12-01 17:34:42','2022-12-01 17:34:42',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,0,0,'2022-12-01 17:34:42','2022-12-01 17:35:31',NULL),(62,NULL,'Samir','BEDOUHENE Samir ',NULL,'samir_ghoucht@hotmail.com','pbkdf2:sha256:260000$RjBj1IQTSko9tKyO$1b5608b9a577b691e85a441a3deb7b19f6792e7b700d2ff60ea70ebce419ae97','client',0,'gratuit','2022-12-04 17:22:37','2022-12-04 17:22:37',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,0,0,'2022-12-04 17:22:37','2022-12-06 16:38:38',NULL),(63,NULL,'Oumayma ','Ramdani oumayma ',NULL,'oumaymaramdani2@gmail.com','pbkdf2:sha256:260000$iV624SAs2HbspRtv$04033a3b85054a2b77f0d629623e927e2b1a7083d95fdb21254f15762428ddf8','client',0,'gratuit','2022-12-07 11:52:46','2022-12-07 11:52:46',1,0,'assets/images/dev/OOjs_UI_icon_userAvatar.svg.png',NULL,0,0,0,'2022-12-07 11:52:46','2022-12-07 11:54:13',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-08 20:15:14

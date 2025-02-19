-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 15, 2025 at 01:26 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `diemdanhsv`
--

-- --------------------------------------------------------

--
-- Table structure for table `dangky`
--

CREATE TABLE `dangky` (
  `HOCKY` varchar(50) DEFAULT NULL,
  `NIENKHOA` varchar(50) DEFAULT NULL,
  `DIEM1` decimal(10,2) DEFAULT NULL,
  `DIEM2` decimal(10,2) DEFAULT NULL,
  `KETQUA` decimal(10,2) DEFAULT NULL,
  `ID_SINHVIEN` int(11) NOT NULL,
  `ID_MON` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `dangky`
--

INSERT INTO `dangky` (`HOCKY`, `NIENKHOA`, `DIEM1`, `DIEM2`, `KETQUA`, `ID_SINHVIEN`, `ID_MON`) VALUES
('hk1', '15', NULL, NULL, NULL, 10, 16),
('hk1', '15', NULL, NULL, NULL, 10, 18),
('hk3', '15', NULL, NULL, NULL, 11, 16),
('3', '3', 10.00, 5.00, 6.50, 12, 19),
('hk2', '16', NULL, NULL, NULL, 14, 19),
('hk2', '16', NULL, NULL, NULL, 14, 20);

-- --------------------------------------------------------

--
-- Table structure for table `diemdanh`
--

CREATE TABLE `diemdanh` (
  `ID_DIEMDANH` int(11) NOT NULL,
  `ID_SINHVIEN` int(11) DEFAULT NULL,
  `ID_MON` int(11) DEFAULT NULL,
  `ID_GIAOVIEN` int(11) DEFAULT NULL,
  `NGAYDIEMDANH` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `giangday`
--

CREATE TABLE `giangday` (
  `ID_GIANGDAY` int(11) NOT NULL,
  `NGAYDAY` date DEFAULT NULL,
  `TIETGD` varchar(100) DEFAULT NULL,
  `ID_GIAOVIEN` int(11) DEFAULT NULL,
  `ID_MON` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `giangday`
--

INSERT INTO `giangday` (`ID_GIANGDAY`, `NGAYDAY`, `TIETGD`, `ID_GIAOVIEN`, `ID_MON`) VALUES
(2, '2025-02-15', '1-2', 2, 16),
(3, '2025-02-15', '1-2', 2, 17),
(4, '2025-02-16', '1-2', 2, 17),
(5, '2025-02-15', 'tiet 3 - 4', 2, 17);

-- --------------------------------------------------------

--
-- Table structure for table `giaovien`
--

CREATE TABLE `giaovien` (
  `ID_GIAOVIEN` int(11) NOT NULL,
  `TENGIAOVIEN` varchar(500) DEFAULT NULL,
  `ID_KHOA` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `giaovien`
--

INSERT INTO `giaovien` (`ID_GIAOVIEN`, `TENGIAOVIEN`, `ID_KHOA`) VALUES
(1, 'giáo viên 1', 1),
(2, 'giáo viên 2', 1),
(3, 'giáo viên 3', 1),
(4, 'giáo viên 5', 1);

-- --------------------------------------------------------

--
-- Table structure for table `khoa`
--

CREATE TABLE `khoa` (
  `ID_KHOA` int(11) NOT NULL,
  `TENKHOA` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `khoa`
--

INSERT INTO `khoa` (`ID_KHOA`, `TENKHOA`) VALUES
(1, 'Kỹ thuật - công nghệ');

-- --------------------------------------------------------

--
-- Table structure for table `lophoc`
--

CREATE TABLE `lophoc` (
  `ID_LOP` int(11) NOT NULL,
  `TENLOP` varchar(200) DEFAULT NULL,
  `ID_KHOA` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `lophoc`
--

INSERT INTO `lophoc` (`ID_LOP`, `TENLOP`, `ID_KHOA`) VALUES
(3, 'Lớp 1', 1),
(4, 'Lớp 2', 1);

-- --------------------------------------------------------

--
-- Table structure for table `lophoc_monhoc`
--

CREATE TABLE `lophoc_monhoc` (
  `ID_LOP` int(11) NOT NULL,
  `ID_MON` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `lophoc_monhoc`
--

INSERT INTO `lophoc_monhoc` (`ID_LOP`, `ID_MON`) VALUES
(3, 16),
(3, 17),
(3, 18),
(4, 19),
(4, 20);

-- --------------------------------------------------------

--
-- Table structure for table `monhoc`
--

CREATE TABLE `monhoc` (
  `ID_MON` int(11) NOT NULL,
  `TENMON` varchar(200) DEFAULT NULL,
  `SOTINCHI` int(11) DEFAULT NULL,
  `ID_GIAOVIEN` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `monhoc`
--

INSERT INTO `monhoc` (`ID_MON`, `TENMON`, `SOTINCHI`, `ID_GIAOVIEN`) VALUES
(16, 'Toán số', 3, 1),
(17, 'Toán hình', 3, 1),
(18, 'Toán xác suất', 3, 2),
(19, 'luật', 2, 3),
(20, 'Quốc phòng', 8, 4);

-- --------------------------------------------------------

--
-- Table structure for table `sinhvien`
--

CREATE TABLE `sinhvien` (
  `ID_SINHVIEN` int(11) NOT NULL,
  `TENSINHVIEN` varchar(200) DEFAULT NULL,
  `NGAYSINH` date DEFAULT NULL,
  `GIOITINH` int(1) DEFAULT NULL,
  `ID_LOP` int(11) DEFAULT NULL,
  `KHUONMAT` longblob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `sinhvien`
--

INSERT INTO `sinhvien` (`ID_SINHVIEN`, `TENSINHVIEN`, `NGAYSINH`, `GIOITINH`, `ID_LOP`, `KHUONMAT`) VALUES
(10, 'hs 1', '2025-02-13', 0, 3, 0xc54eeca47bdfbcbf8a9dd869251abd3f9ed8896daa52b23f4fecc4ae7fe6a7bf000000901f8aa4bfd9899d98605db0bf622776c213eeb6bf000000e034f3bebf3bb113fba42cc33f76622776e5d2bbbf766227962b87d23f9ed88995382998bf3bb1137bca1fc9bf4fecc4aee923c5bfecc44e24629891bf4fecc42eed94c53f9ed8895dc791c9bfb1133b11611fb8bf8a9dd809767d853f2776628714a88abfecc44ecc037fb93f4fecc4aed5b36fbfecc44e4cb5dea83f277662276eb0913fecc44e4c2febc1bf143bb1f3f03dd8bf3bb1135b3263bbbfecc44e0c80b7bcbfb1133b11d10aae3f3bb113bbd298b4bf6227762247d7a8bf4fecc41e1e31a3bf9ed889dd005bc9bf143bb1732c83b0bf766227464c09943fc54eec44bec8ac3f000000000c9ba9bf27766297ef61b0bf766227f66d61c53fc54eec442c27583f62277622617cccbf622776623602a1bfd9899d5878e4a4bf9ed8899dd866c93f4fecc40edfdebe3f3bb113dbb5009c3f8a9dd8a9f132b03fc54eeca4d7b5c5bf76622776e318c23f62277662ab65c2bf143bb1532608aa3f76622726eecfc03fb1133b111eeca43f766227f67688b13f4fecc4be588d93bf62277622fad6c0bf766227761b0f55bf3bb1135bf7cac23fecc44e8c015cc9bf622776a2ec98933f143bb103228ca33f277662a7c65eb5bf9ed8890dd629a0bf9ed8899d9d459dbfc54eeca44826c73f3bb1131bc30bb93f4fecc40e771bc1bf3bb1131b98bec8bf7662273665c1be3fd9899d789ef4babfc54eecc450f264bf00000020e953bb3f8a9dd8896ddebebf9ed889dd0a19ccbf8a9dd8093965d2bf622776e2bd69a23fc54eec0435cbd93f9ed8893d7927ad3f4fecc45ea5dac0bf277662277539493fd9899d38d0d7babf6227764234d8a9bf9ed8895dd95fba3f000000a088f8c43f9ed8899d3e0d793f3bb1133b8030aa3f76622736705ca7bf8a9dd8a90d87a93f143bb1d3ca88c73f8a9dd8090ae4b8bf000000a08137a1bf143bb193ea69ca3f8a9dd889a083adbfb1133b51958fc43fc54eec0485698cbfc54eec84dc81ac3fb1133b111e45babf8a9dd82990a7b53fc54eec442865a0bf0000000043e5683fb1133b11c1f2a93f76622736febd95bfc54eec04f202903f622776a20c85b43f8a9dd8494cf8bdbf8a9dd8298ed1c13fb1133b213d41a93f000000d0baf39d3fecc44eec3412a13f622776020b7395bf9ed889fd4b3bb3bf143bb1f38cf5babf4fecc48ef851b83f8a9dd8a9afcbcfbf9ed889fd5cd9d13f8a9dd8494097ca3fd9899d6816ecb43f766227d66bcac43f3bb1139bc98fb83f00000070d2439c3f00000070ab8d923fd9899d384d8bb3bf143bb11393a8c7bfc54eec047a1f9c3f8a9dd8399c19b43fb1133b41d0f787bf143bb19305acad3fd9899d285455b1bf),
(11, 'hs 2', '2025-02-13', 1, 3, 0xcdcccc2cdc55c7bfcdcccc4cc69dbd3f333333fbaa63b03f9a9999a9a668b9bf666666e6dbd3c4bfcdccccac9c21b8bf000000604d8cb0bf666666e6eedababf666666167592bc3f6666664e6dc8b3bf33333383d46ad13f000000c07a7ec1bf000000d0b790cdbf333333639e8db2bf666666162ed6b5bf666666b6b202ce3f66666676754acdbf000000400aa2c1bf9a999951d593a2bf66666686630b853f9a9999c10f83b03f66666616b7f0a0bf6666667eeaee78bf000000b013deac3fcdcccc2c22a4c6bfcdcccc3cb5d8d7bf333333033c4daabf000000b8490bb0bf66666626ea4cb7bfcdcccccca822a0bf9a9999191c9d9f3f00000060206eaf3fcdcccc5c11f7cbbfcdccccb419a9a5bf666666162369a23f333333b3103bb73f666666b67dfc8abf000000e0330ca6bf333333d3c676c03f666666669335a9bf00000070b66cd2bf66666686584894bf66666696c2b3bb3f333333cba084d03f000000106b9bc53f3333336fe2168c3f9a999911af0da53f6666660eaf39c1bf000000b0eea9bd3f000000b0cfdec5bf00000000a703a6bf00000090daecc33f33333323280185bf000000885d6d983f33333373970773bf00000010c818b9bf666666265876a13f333333a37f4dc73f9a9999f96d35bdbf666666aae96399bf3333336b318ac03f333333d3f55cb3bf666666665c4029bf9a999999c276c3bf000000901776d23f9a9999314c5e923fcdcccc7c2d27c5bf333333134584c3bf66666666f66cbe3f33333353c91db9bf6666667617b1a8bfcdcccc3c2b2da83f66666666fa15c6bf000000e0cc41ccbfcdccccfce14ad6bf9a99992937af8f3fcdcccccc708fd63f9a9999197cbbb53f3333334bf95ec0bfcdcccc04b352b33f3333337b315cb1bfcdcccc6c42a59b3f66666646db6eb13f9a9999a9e4b4c63f9a9999b9dd45973fcdcccc2cc78ab43f666666f66cf4b7bf666666ce0b08953fcdcccc544543d03f9a9999a90ceab7bf6666663685bea83f66666676bcc4cf3fcdcccc0c3cd0a0bf666666b60611913f9a9999e96bd194bf333333757f199dbfcdccccccc1a5c0bf66666646a2d4a43f66666606d0c7bcbf333333a7e7ae983fcdcccccc64db333f00000048ebffa0bf00000080b0b48d3fcdccccfcf163b83f9a9999299d09c1bf9a999999e9a4b03f00000078898c7cbf333333eb8d1cb43fcdcccc146b7aa3bf9a9999d16c8c7dbf00000050f2a4a9bf333333b3e52bc0bf33333393c5b7bb3fcdcccc8c0acbc7bf000000f0f63fca3f000000f01c4cc53f000000a033f1bc3f666666962212bc3f000000301498c43f3333333b4465a53f33333333d48c99bfcdcccc2c2a78a23f66666666acc2c2bf00000070717ca43fcdcccc9ca9a7bb3f9a999999c736b5bfcdcccc4cb17bbd3f9a9999f110e287bf),
(12, 'hs 3', '2025-02-13', 1, 3, 0x3bb113bba155c7bfc54eecc45d74ac3f3bb1136b1464a03f622776824510bbbf62277622ece6b5bf4fecc48eaea3a8bfd9899db868f595bf766227367854c0bf00000080154abd3f143bb153eb4eb7bfc54eec34798fd13fd9899d380dd9b4bf766227f6bc86c6bf143bb1d31a34bcbf3bb1131b4566acbf143bb1d3b954c33fb1133b3169b3c6bf3bb1135bba68a9bf277662673cd6b4bf0000007044b999bf62277632ebfd993f4fecc4ce7af9aabf143bb16b5f3792bf000000102f0aa43f622776c21f07a6bfc54eec84ae93d5bf7662271687a6b0bf277662e7a5f0a5bf76622776a86c643f143bb163478f98bfd9899d18acaca6bfc54eec376d1b9b3f9ed8899dd0b9c8bf9ed8893d9ddebbbf9ed8891deb0987bf622776d2e90cb33f8a9dd88941d79bbf3bb1134b9968a1bfecc44e2ca587c03f76622716d33bafbf766227565849c6bf143bb1bb5efc83bfd9899d78d9c7ae3fecc44e6cfddece3fc54eec644369cb3f00000040b4cab03f9ed889b560caa2bfb1133bf19c2eb6bf8a9dd849a9fcc23f000000205d88ccbf4fecc44e3d72a23f000000404f62b83f3bb113fbf50cb83f277662274bdba83f9ed889fd13f383bf4fecc46e71c8b2bf143bb123eb94943f143bb1536732c43f9ed8899dd903c3bf62277692712b90bfecc44e0cfd7eab3fc54eecf4ea33b7bf3bb1131bcdbcadbfd9899d182a8eb7bf143bb153cab9ce3fecc44eac4b78c43fecc44ebcf3a7c1bf4fecc40e4bf5b8bfc54eecc4dc5fbe3f000000c0c0eab4bf0000004ca1c6a0bfd9899d88dd4f91bf27766227cf97c1bfb1133b718b33c9bf8a9dd8c98619d2bfb1133b914bc3b53f9ed8897d408dd43fd9899d987eb8c13fb1133b3133a8c6bf622776c2b78c94bf000000408e1cb4bfc54eec94030ca83f7662271626c0c23fecc44e4cef19b43fecc44eec8beea0bf9ed8893d4cd495bfc54eeca47fb3a8bf3bb1137ba2377b3fb1133b71a1dfc43f277662a7c867adbf00000050c294a4bfd9899d38f05ecc3fc54eecd40c6d98bfc54eec04d1ac943f9ed8899da3085c3f4fecc44eea18ad3f9ed8891d4061abbfd9899d48a0edaa3f27766227ff1ac2bf143bb1d3d2256d3fecc44e4c98e1c33f00000050a06a9cbf143bb1b3dc87ae3f000000a054d8b93f9ed8891d3836c6bf8a9dd829a2c7bf3f766227b6a291573fecc44eac5a60b63f9ed889fde091b93f9ed8893dd2cbb3bfc54eecd42e6698bf000000207cf0aabf143bb11389dab93f4fecc46e267cc6bfb1133b318359ce3f4fecc4ae7288c43f8a9dd82b780ca23f8a9dd889c1c9c33fecc44eec06bfba3f766227c63a049c3f9ed8899d8f6f933fd9899d18c2f192bf277662674f57c1bf000000a0a7ed97bf4fecc4ee266cbf3f3bb1135bd0c77f3f8a9dd8a9fbaaba3f62277622c6476b3f),
(13, 'hs 4', '2025-02-13', 1, 4, 0x8a9dd8e94834a7bf4fecc4ae5931a43fb1133b911698723f277662ff932c87bf6227768221e3b2bf9ed8892dca42b1bfecc44eac2b47ae3f6227768281dabebf143bb193615ab93f9ed8891d84c5a5bf4fecc48ed5d9d03fb1133b113ccaacbf3bb1137b849ecfbf766227b6dcb8bfbf8a9dd8695177b6bf9ed8899dea42c93fecc44ecc71d7c7bfecc44e2c2bbebbbfecc44e8cd402a9bfb1133b0130a29b3f62277602fb1fc03f6227767ac76981bfd9899d78fe12993f9ed8897df2a4a13fd9899d58d37c793f6227768259c8d3bf000000e0c579bbbf4fecc4eef201b4bf3bb113dbd94a9b3f8a9dd829837ba9bf6227762200c070bfb1133b71725faf3f3bb1135bd840c8bf62277682ac80b8bfb1133b51185ba13f76622756c142a03fb1133b21ab48a4bf00000010088fa2bf27766227d0c1ca3f27766247a9e198bf3bb1135ba7a4c9bf9ed8891ddd018ebf277662273d2db93fc54eec145d77d03f766227761732c23f8a9dd809375eb63fb1133b718dc787bf76622796f6f3bbbf4fecc46e4da2a53fc54eec04b82ac5bf8a9dd8d93307a53f000000804613bc3fecc44ecc2aacc43f143bb133c1479b3f4fecc41e18f7863fc54eecc4dad0bebf8a9dd8c9be24a23fc54eec84bf66bc3f4fecc42e9f42c9bfc54eec04e57068bf76622706bfceb33f62277682e7f3b7bf277662f75641a1bf143bb1b379c3b4bfc54eecc4bd2fce3f622776b2038c933f766227b6eb62babf143bb1737744c1bf4fecc4ce66dfc13f8a9dd8295884c1bf4fecc48e04a1b6bfb1133b51fa40a23f766227165807c2bfd9899d783ad7c4bfb1133bd126ced3bf4fecc44eb892543f00000020cb48d83fb1133b710b01ae3f8a9dd84981c8c2bf8a9dd8c9a49bad3f4fecc48ebfb69bbf9ed8891d20817cbf766227a6deb2c13f9ed889dddf1fb73fb1133b01d97d96bfecc44e0c111e953f9ed8895ded79c1bf62277662bc0a773f9ed8896db50dc13fd9899d587d85bdbf277662e70d3ea2bf143bb13372a3c43f143bb1135c89abbf622776b266c4973f0000008089e7883f76622776bbb578bf143bb1f36c0a82bf4fecc44ec0a6b93fd9899dd81241c2bf6227766217735bbf622776a20617b03f766227568d0fa7bf766227e6a9da903f27766267046fb43f27766207eabfbdbf143bb1f3374b783f3bb113cb095d7abfecc44eac0138863fd9899df8f3d8953fb1133b219e9ab2bfc54eec84ed95c4bfd9899dd8d2bfaebf622776426394bd3f4fecc44ef369cdbf000000e079c3ce3f4fecc46e728cc33f766227ee7ab692bfd9899d987566af3fb1133b11b24eb73f27766227db31b63f76622726a4bd90bfc54eec045f2fb2bfb1133bf1ee28d0bf8a9dd82158bc82bf00000020a459c53fecc44e3c40629abfc54eec842187bf3f76622716860098bf),
(14, 'hs 5', '2025-02-13', 0, 4, 0x6227768283deadbf8a9dd8498ffba73f4fecc41ea7138c3f3bb113ab2cc57fbfecc44eac7bb9aebf277662a72b23b5bf8a9dd8491fe2af3f000000a07a09bfbfecc44e8c0e0bbc3f62277652822fa0bf143bb1532ca9cf3f143bb1b3c62fb5bf8a9dd809b941cebfc54eeca4c7f8c1bfecc44e0c9bb9b3bf143bb15323b4ca3f4fecc46ea045c9bf000000a01a58bcbfb1133b51df65a7bf3bb113db926b963f4fecc4ae99bfbf3f622776aae23f88bfd9899d188a649b3f27766247f6b4ae3fb1133bb1cf6047bfecc44e8c9cfed4bf622776421b80bcbf143bb1d36ce6b8bf766227b6e49aa03fd9899dd88b55a8bf143bb11331fd96bf9ed8895d654fb13f3bb113dbe369c7bf9ed889fd1714bbbfb1133bf10dae9d3f8a9dd889b7f69f3f4fecc4ae44939ebf766227965ea5a3bf622776424288c93f9ed8893d14a5a5bfecc44e0c7340cabf2776625f19b991bfd9899df832d1bb3f8a9dd809b884d03f000000c09fe2c23fc54eec64e275b53f143bb193e09d79bf9ed889fd8904b9bf00000000078ca23fd9899d38ec68c4bf622776a25d45ac3f000000406c07bc3f9ed889fda7d9c13f277662a7fd379d3f00000040c1e6953f143bb193e157bdbf143bb1531571963f9ed8893da537bc3f3bb1139b7353c9bf8a9dd859bf95853f62277622df72b53f000000e0531cb8bf9ed889bd6ae6abbfd9899db8710db3bf766227f658eacc3fc54eec1410cea23f143bb1b3ced5b8bf4fecc40ef089c3bf8a9dd849d90ac23fb1133b713709c3bf766227d6b3e0b5bf3bb113fbd3ff9f3f000000806bdbc2bf8a9dd8093bb1c3bf143bb1f3a2a4d4bf277662676ed7843f9ed8895d2043d83f9ed8897d2c23a93fc54eecc405cfc2bfc54eecc4e068b13fb1133b31ef8d93bf00000020325e75bfc54eec8425e2c23f00000080245dba3f277662a730cd91bfb1133b1181b1913f000000e036fec0bfc54eec64dac68e3f3bb1131b77c8bd3f4fecc40e95d1babf4fecc4fea4a8a1bf000000407df0c33fd9899d38b953adbfd9899d98489a893fb1133bc15bd3813f4fecc4ce32c159bfb1133b71742072bf3bb1137be89eba3fc54eec84135fc2bfd9899d58b2fb723fb1133b51496cb73fd9899db88f719dbf3bb113fb03ab753fb1133b919d89b43fd9899dd82879bdbfecc44eecbcda273fb1133b31b7546f3f4fecc4aed329883f9ed889fd40649e3f143bb1a32f4ab0bf9ed889bd3c3fc5bf8a9dd859e183b0bfecc44ecc5a55be3fb1133b31274fccbf62277622eb66ce3fc54eece4bf9ec33f622776c2e41a8ebfecc44e8cd07aac3f000000204c92b33f76622776af7bb63f0000000038fe25bf622776922566b1bfecc44e9c7025d0bfd9899d100dda6d3f9ed8897dcb09c73fb1133b915c0c9cbfd9899db8b382bb3f9ed889bd685793bf);

-- --------------------------------------------------------

--
-- Table structure for table `taikhoangv`
--

CREATE TABLE `taikhoangv` (
  `ID_TKGV` int(11) NOT NULL,
  `USERNAME` varchar(200) DEFAULT NULL,
  `PASSWORD` varchar(200) DEFAULT NULL,
  `QUYENHAN` varchar(200) DEFAULT NULL,
  `ID_GIAOVIEN` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `taikhoangv`
--

INSERT INTO `taikhoangv` (`ID_TKGV`, `USERNAME`, `PASSWORD`, `QUYENHAN`, `ID_GIAOVIEN`) VALUES
(1, 'hovtoi', '12345', 'teacher', 1),
(2, 'toi', 'toi', '0', 2);

-- --------------------------------------------------------

--
-- Table structure for table `taikhoansv`
--

CREATE TABLE `taikhoansv` (
  `ID_TKSV` int(11) NOT NULL,
  `USERNAME` varchar(200) DEFAULT NULL,
  `PASSWORD` varchar(200) DEFAULT NULL,
  `ID_SINHVIEN` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `taikhoansv`
--

INSERT INTO `taikhoansv` (`ID_TKSV`, `USERNAME`, `PASSWORD`, `ID_SINHVIEN`) VALUES
(3, 'toi', 'toi', 10),
(4, 'khang', '123', 14),
(5, 'hs2', '123', 11),
(6, 'hs3', '123', 12);

-- --------------------------------------------------------

--
-- Table structure for table `thongbao`
--

CREATE TABLE `thongbao` (
  `id` int(11) NOT NULL,
  `tieude` varchar(255) DEFAULT NULL,
  `noidung` text DEFAULT NULL,
  `ngaydang` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `thongbao`
--

INSERT INTO `thongbao` (`id`, `tieude`, `noidung`, `ngaydang`) VALUES
(1, 'Thông báo 1', 'Nội dung thông báo 1', '2024-02-10'),
(2, 'Thông báo 2', 'Nội dung thông báo 2', '2024-02-09');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `dangky`
--
ALTER TABLE `dangky`
  ADD PRIMARY KEY (`ID_SINHVIEN`,`ID_MON`),
  ADD KEY `ID_MON` (`ID_MON`);

--
-- Indexes for table `diemdanh`
--
ALTER TABLE `diemdanh`
  ADD PRIMARY KEY (`ID_DIEMDANH`),
  ADD KEY `ID_SINHVIEN` (`ID_SINHVIEN`),
  ADD KEY `ID_MON` (`ID_MON`),
  ADD KEY `ID_GIAOVIEN` (`ID_GIAOVIEN`);

--
-- Indexes for table `giangday`
--
ALTER TABLE `giangday`
  ADD PRIMARY KEY (`ID_GIANGDAY`),
  ADD KEY `ID_GIAOVIEN` (`ID_GIAOVIEN`),
  ADD KEY `ID_MON` (`ID_MON`);

--
-- Indexes for table `giaovien`
--
ALTER TABLE `giaovien`
  ADD PRIMARY KEY (`ID_GIAOVIEN`),
  ADD KEY `ID_KHOA` (`ID_KHOA`);

--
-- Indexes for table `khoa`
--
ALTER TABLE `khoa`
  ADD PRIMARY KEY (`ID_KHOA`);

--
-- Indexes for table `lophoc`
--
ALTER TABLE `lophoc`
  ADD PRIMARY KEY (`ID_LOP`),
  ADD KEY `ID_KHOA` (`ID_KHOA`);

--
-- Indexes for table `lophoc_monhoc`
--
ALTER TABLE `lophoc_monhoc`
  ADD PRIMARY KEY (`ID_LOP`,`ID_MON`),
  ADD KEY `ID_MON` (`ID_MON`);

--
-- Indexes for table `monhoc`
--
ALTER TABLE `monhoc`
  ADD PRIMARY KEY (`ID_MON`),
  ADD KEY `fk_giaovien` (`ID_GIAOVIEN`);

--
-- Indexes for table `sinhvien`
--
ALTER TABLE `sinhvien`
  ADD PRIMARY KEY (`ID_SINHVIEN`),
  ADD KEY `fk_sinhvien_lophoc` (`ID_LOP`);

--
-- Indexes for table `taikhoangv`
--
ALTER TABLE `taikhoangv`
  ADD PRIMARY KEY (`ID_TKGV`),
  ADD KEY `ID_GIAOVIEN` (`ID_GIAOVIEN`);

--
-- Indexes for table `taikhoansv`
--
ALTER TABLE `taikhoansv`
  ADD PRIMARY KEY (`ID_TKSV`),
  ADD KEY `ID_SINHVIEN` (`ID_SINHVIEN`);

--
-- Indexes for table `thongbao`
--
ALTER TABLE `thongbao`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `diemdanh`
--
ALTER TABLE `diemdanh`
  MODIFY `ID_DIEMDANH` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `giangday`
--
ALTER TABLE `giangday`
  MODIFY `ID_GIANGDAY` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `giaovien`
--
ALTER TABLE `giaovien`
  MODIFY `ID_GIAOVIEN` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `khoa`
--
ALTER TABLE `khoa`
  MODIFY `ID_KHOA` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `lophoc`
--
ALTER TABLE `lophoc`
  MODIFY `ID_LOP` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `monhoc`
--
ALTER TABLE `monhoc`
  MODIFY `ID_MON` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `sinhvien`
--
ALTER TABLE `sinhvien`
  MODIFY `ID_SINHVIEN` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `taikhoangv`
--
ALTER TABLE `taikhoangv`
  MODIFY `ID_TKGV` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `taikhoansv`
--
ALTER TABLE `taikhoansv`
  MODIFY `ID_TKSV` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `thongbao`
--
ALTER TABLE `thongbao`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `dangky`
--
ALTER TABLE `dangky`
  ADD CONSTRAINT `dangky_ibfk_1` FOREIGN KEY (`ID_SINHVIEN`) REFERENCES `sinhvien` (`ID_SINHVIEN`),
  ADD CONSTRAINT `dangky_ibfk_2` FOREIGN KEY (`ID_MON`) REFERENCES `monhoc` (`ID_MON`);

--
-- Constraints for table `diemdanh`
--
ALTER TABLE `diemdanh`
  ADD CONSTRAINT `diemdanh_ibfk_1` FOREIGN KEY (`ID_SINHVIEN`) REFERENCES `sinhvien` (`ID_SINHVIEN`),
  ADD CONSTRAINT `diemdanh_ibfk_2` FOREIGN KEY (`ID_MON`) REFERENCES `monhoc` (`ID_MON`),
  ADD CONSTRAINT `diemdanh_ibfk_3` FOREIGN KEY (`ID_GIAOVIEN`) REFERENCES `giaovien` (`ID_GIAOVIEN`);

--
-- Constraints for table `giangday`
--
ALTER TABLE `giangday`
  ADD CONSTRAINT `giangday_ibfk_1` FOREIGN KEY (`ID_GIAOVIEN`) REFERENCES `giaovien` (`ID_GIAOVIEN`),
  ADD CONSTRAINT `giangday_ibfk_2` FOREIGN KEY (`ID_MON`) REFERENCES `monhoc` (`ID_MON`);

--
-- Constraints for table `giaovien`
--
ALTER TABLE `giaovien`
  ADD CONSTRAINT `giaovien_ibfk_1` FOREIGN KEY (`ID_KHOA`) REFERENCES `khoa` (`ID_KHOA`);

--
-- Constraints for table `lophoc`
--
ALTER TABLE `lophoc`
  ADD CONSTRAINT `lophoc_ibfk_1` FOREIGN KEY (`ID_KHOA`) REFERENCES `khoa` (`ID_KHOA`);

--
-- Constraints for table `lophoc_monhoc`
--
ALTER TABLE `lophoc_monhoc`
  ADD CONSTRAINT `lophoc_monhoc_ibfk_1` FOREIGN KEY (`ID_LOP`) REFERENCES `lophoc` (`ID_LOP`),
  ADD CONSTRAINT `lophoc_monhoc_ibfk_2` FOREIGN KEY (`ID_MON`) REFERENCES `monhoc` (`ID_MON`);

--
-- Constraints for table `monhoc`
--
ALTER TABLE `monhoc`
  ADD CONSTRAINT `fk_giaovien` FOREIGN KEY (`ID_GIAOVIEN`) REFERENCES `giaovien` (`ID_GIAOVIEN`) ON DELETE CASCADE;

--
-- Constraints for table `sinhvien`
--
ALTER TABLE `sinhvien`
  ADD CONSTRAINT `fk_sinhvien_lophoc` FOREIGN KEY (`ID_LOP`) REFERENCES `lophoc` (`ID_LOP`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `taikhoangv`
--
ALTER TABLE `taikhoangv`
  ADD CONSTRAINT `taikhoangv_ibfk_1` FOREIGN KEY (`ID_GIAOVIEN`) REFERENCES `giaovien` (`ID_GIAOVIEN`);

--
-- Constraints for table `taikhoansv`
--
ALTER TABLE `taikhoansv`
  ADD CONSTRAINT `taikhoansv_ibfk_1` FOREIGN KEY (`ID_SINHVIEN`) REFERENCES `sinhvien` (`ID_SINHVIEN`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

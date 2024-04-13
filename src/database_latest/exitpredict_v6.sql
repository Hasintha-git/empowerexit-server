-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 04, 2023 at 05:52 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `exitpredict`
--

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

CREATE TABLE `department` (
  `id` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  `created_timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `department`
--

INSERT INTO `department` (`id`, `name`, `created_timestamp`) VALUES
(1, 'Food and Beverages', '2023-01-21 01:36:20'),
(2, 'Front Office', '2023-01-21 12:23:21'),
(3, 'Housekeeping', '2023-02-26 13:24:21'),
(4, 'Maintenance', '2023-02-26 13:24:21'),
(5, 'Security', '2023-02-26 13:24:21');

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `id` int(11) NOT NULL,
  `emp_id` varchar(45) NOT NULL,
  `name` varchar(45) NOT NULL,
  `designation` varchar(45) NOT NULL,
  `fk_department_id` int(11) NOT NULL,
  `address` varchar(45) NOT NULL,
  `contact` varchar(45) NOT NULL,
  `supervisor` varchar(45) NOT NULL,
  `joined_date` date NOT NULL,
  `performance_grade` varchar(45) NOT NULL,
  `note` varchar(1000) DEFAULT NULL,
  `is_leaving` tinyint(4) DEFAULT 0,
  `latest_turnover_rate` varchar(20) DEFAULT '-',
  `latest_months_to_leave` varchar(20) DEFAULT '-',
  `created_timestamp` datetime NOT NULL,
  `updated_timestamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`id`, `emp_id`, `name`, `designation`, `fk_department_id`, `address`, `contact`, `supervisor`, `joined_date`, `performance_grade`, `note`, `is_leaving`, `latest_turnover_rate`, `latest_months_to_leave`, `created_timestamp`, `updated_timestamp`) VALUES
(29, 'emp_01', 'Prashan Rathnayake', 'Waiter', 1, '123, colombo', '077123456', 'N/A', '2022-12-22', 'A', '', 1, '0.5454545454545454', '4', '2023-03-13 15:42:36', '2023-04-02 20:31:49'),
(34, 'emp_02', 'Amasha Perera', 'Engineer', 1, '123, colombo', '0771234567', '0771234567', '2022-11-22', 'A', NULL, 1, '0.5303030303030302', '3', '0000-00-00 00:00:00', '2023-03-21 10:10:43'),
(36, 'emp_04', 'Amsha Munasinghe', 'Admin', 2, '123, colombo', '077123456', 'N/A', '2022-12-12', 'A', '', 1, '0.6212121212121212', '3', '2023-03-21 00:39:55', '2023-03-21 10:13:26'),
(37, 'emp_05', 'Amal Perera', 'Admin', 2, '123, colombo', '077123456', 'N/A', '2022-12-12', 'A', '', 1, '0.5454545454545454', '3', '2023-03-21 00:40:17', '2023-03-21 10:49:45'),
(38, 'emp_06', 'Kamla Peries', 'Admin', 4, '123, colombo', '077123456', 'N/A', '2022-12-12', 'A', '', 1, '0.5454545454545454', '3', '2023-03-21 00:40:50', '2023-03-21 10:50:20'),
(39, 'emp_07', 'Nirmala Peries', 'Admin', 5, '123, colombo', '077123456', 'N/A', '2022-12-12', 'A', '', 1, '0.5454545454545454', '3', '2023-03-21 00:41:29', '2023-03-21 10:50:24'),
(40, 'emp_08', 'Nikila Peries', 'Admin', 5, '123, colombo', '077123456', 'N/A', '2022-12-12', 'A', '', 1, '0.5454545454545454', '3', '2023-03-21 00:42:11', '2023-03-21 10:50:27'),
(45, 'emp_21', 'Aruna Pathirana', 'Engineer', 4, '123, perera mawatha', '0777777777', 'NA', '2020-10-12', 'A', '', 1, '0.5454545454545454', '1', '2023-03-23 02:58:45', '2023-03-30 10:29:27'),
(46, 'emp_90', 'Latha Walpola', 'Security', 5, '123, Sarankara Mawatha, Karagamapitiya', '0771234567', 'N/A', '2022-09-08', 'D', '', 0, '0', '0', '2023-03-29 19:45:24', '2023-03-29 19:45:24'),
(50, '112', 'dfsadcsx', 'sadasd', 3, 'aadasd', 'asdas', 'asdasd', '2023-04-25', 'B', '', 0, '-', '-', '2023-04-02 12:20:43', '2023-04-02 12:20:43'),
(51, '444', '4444', 'buu', 2, '44', '444', '44', '2023-04-24', 'B', '', 0, '-', '-', '2023-04-02 16:27:45', '2023-04-02 16:28:19');

-- --------------------------------------------------------

--
-- Table structure for table `prediction`
--

CREATE TABLE `prediction` (
  `id` int(11) NOT NULL,
  `fk_emp_id` int(11) NOT NULL,
  `is_leaving` tinyint(4) DEFAULT NULL,
  `turnover_rate` varchar(20) NOT NULL,
  `month_to_leave` int(11) DEFAULT NULL,
  `created_timestamp` datetime DEFAULT NULL,
  `updated_timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prediction`
--

INSERT INTO `prediction` (`id`, `fk_emp_id`, `is_leaving`, `turnover_rate`, `month_to_leave`, `created_timestamp`, `updated_timestamp`) VALUES
(26, 29, 1, '0.606060606060606', 4, '2023-02-21 10:07:52', '2023-03-21 10:07:52'),
(27, 29, 1, '0.5454545454545454', 5, '2023-03-21 10:09:29', '2023-04-21 10:09:43'),
(28, 34, 1, '0.5303030303030302', 3, '2023-03-21 10:10:43', '2023-04-21 10:10:43'),
(30, 36, 1, '0.6212121212121212', 3, '2023-03-21 10:13:26', '2023-04-21 10:13:26'),
(31, 37, 1, '0.5454545454545454', 3, '2023-03-21 10:14:01', '2023-04-21 10:49:45'),
(32, 38, 1, '0.5454545454545454', 3, '2023-03-21 10:50:20', '2023-04-21 10:50:20'),
(33, 39, 1, '0.5454545454545454', 3, '2023-03-21 10:50:24', '2023-04-21 10:50:24'),
(34, 40, 1, '0.5454545454545454', 3, '2023-03-21 10:50:27', '2023-04-21 10:50:27'),
(37, 45, 1, '0.5454545454545454', 1, '2023-03-30 10:18:48', '2023-04-30 10:29:27');

-- --------------------------------------------------------

--
-- Table structure for table `prediction_factor_mapping`
--

CREATE TABLE `prediction_factor_mapping` (
  `id` int(11) NOT NULL,
  `fk_prediction_id` int(11) NOT NULL,
  `fk_factor_id` int(11) NOT NULL,
  `score` varchar(20) DEFAULT NULL,
  `created_timestamp` datetime DEFAULT NULL,
  `updated_timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prediction_factor_mapping`
--

INSERT INTO `prediction_factor_mapping` (`id`, `fk_prediction_id`, `fk_factor_id`, `score`, `created_timestamp`, `updated_timestamp`) VALUES
(1, 26, 22, '0.2747774502749651', '2023-02-21 10:07:54', '2023-03-21 10:07:54'),
(2, 26, 18, '0.016337657777972525', '2023-02-21 10:07:54', '2023-03-21 10:07:54'),
(3, 26, 21, '0.011328818987713807', '2023-02-21 10:07:54', '2023-03-21 10:07:54'),
(7, 27, 22, '0.2220671933100885', '2023-03-21 10:09:43', '2023-03-21 10:09:43'),
(8, 27, 18, '0.01536274741997399', '2023-04-21 10:09:43', '2023-04-21 10:09:43'),
(9, 27, 1, '0.008580820688868047', '2023-03-21 10:09:43', '2023-04-21 10:09:43'),
(10, 28, 22, '0.1865552716447071', '2023-03-21 10:10:43', '2023-04-21 10:10:43'),
(11, 28, 20, '0.019581031864413515', '2023-03-21 10:10:43', '2023-04-21 10:10:43'),
(12, 28, 1, '0.00888959094602806', '2023-03-21 10:10:43', '2023-04-21 10:10:43'),
(19, 30, 22, '0.22134021768380133', '2023-03-21 10:13:26', '2023-04-21 10:13:26'),
(20, 30, 18, '0.016019447177183392', '2023-03-21 10:13:26', '2023-04-21 10:13:26'),
(21, 30, 15, '0.008040260602368099', '2023-03-21 10:13:26', '2023-04-21 10:13:26'),
(78, 31, 22, '0.238213508906995', '2023-03-21 10:49:45', '2023-04-21 10:49:45'),
(79, 31, 15, '0.008529179662598219', '2023-03-21 10:49:45', '2023-04-21 10:49:45'),
(80, 31, 69, '0.006169900767082142', '2023-03-21 10:49:45', '2023-04-21 10:49:45'),
(81, 32, 22, '0.23822123975648948', '2023-03-21 10:50:20', '2023-04-21 10:50:20'),
(82, 32, 15, '0.008440542194866953', '2023-03-21 10:50:20', '2023-04-21 10:50:20'),
(83, 32, 69, '0.006169900767082142', '2023-03-21 10:50:20', '2023-04-21 10:50:20'),
(84, 33, 22, '0.23822123975648948', '2023-03-21 10:50:24', '2023-04-21 10:50:24'),
(85, 33, 15, '0.008440542194866953', '2023-03-21 10:50:24', '2023-04-21 10:50:24'),
(86, 33, 69, '0.00564707405604525', '2023-03-21 10:50:24', '2023-04-21 10:50:24'),
(87, 34, 22, '0.23822123975648948', '2023-03-21 10:50:27', '2023-04-21 10:50:27'),
(88, 34, 15, '0.008440542194866953', '2023-03-21 10:50:27', '2023-04-21 10:50:27'),
(89, 34, 69, '0.00564707405604525', '0000-00-00 00:00:00', '2023-04-21 10:50:27'),
(107, 37, 22, '0.23822123975648948', '2023-03-30 10:29:27', '2023-03-30 10:29:27'),
(108, 37, 15, '0.008440542194866953', '2023-03-30 10:29:27', '2023-03-30 10:29:27'),
(109, 37, 69, '0.006169900767082142', '2023-03-30 10:29:27', '2023-03-30 10:29:27');

-- --------------------------------------------------------

--
-- Table structure for table `turnover_factor`
--

CREATE TABLE `turnover_factor` (
  `id` int(11) NOT NULL,
  `factor` varchar(45) NOT NULL,
  `display_name` varchar(45) DEFAULT NULL,
  `measure` varchar(500) DEFAULT NULL,
  `created_timestamp` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `turnover_factor`
--

INSERT INTO `turnover_factor` (`id`, `factor`, `display_name`, `measure`, `created_timestamp`) VALUES
(1, 'working_hours', 'Working Hours', 'Offer flexible work schedules', '2023-02-24 15:58:30'),
(2, 'promotional_barriers', 'Promotional Barriers', 'Establish transparent promotion criteria', '2023-02-24 15:58:30'),
(3, 'work_life_balance', 'Work Life Balance', 'work_life_balance measure', '2023-02-24 15:58:30'),
(4, 'status_and_recognition', 'Status and Recognition', 'status_and_recognition measure', '2023-02-24 15:58:30'),
(5, 'salary', 'Salary', 'salary measure', '2023-02-24 15:58:30'),
(6, 'opportunities', 'Opportunities', 'opportunities measure', '2023-02-24 15:58:30'),
(7, 'workload', 'Workload', 'workload measure', '2023-02-24 15:58:30'),
(8, 'work_environment', 'Work Environment', 'work_environment measure', '2023-02-24 15:58:30'),
(9, 'training_and_development', 'Training and Development', 'training_and_development measure', '2023-02-24 15:58:30'),
(10, 'relationship_with_colleagues', 'Relationship with Colleagues', 'relationship_with_colleagues measure', '2023-02-24 15:58:30'),
(11, 'relationship_with_supervisor', 'Relationship with Supervisor', 'relationship_with_supervisor measure', '2023-02-24 15:58:30'),
(12, 'job_satisfaction', 'Job Satisfaction', 'job_satisfaction measure', '2023-02-24 15:58:30'),
(13, 'age', 'Age', 'age measure', '2023-02-26 08:04:39'),
(14, 'gender', 'Gender', 'gender measure', '2023-02-26 08:05:32'),
(15, 'marital_status', 'Marital Status', 'marital_status measure', '2023-02-26 08:06:18'),
(16, 'educational_status', 'Educational Status', 'educational_status measure', '2023-02-26 08:06:18'),
(17, 'total_years_industry', 'Total Years in Industry', 'total_years_industry measure', '2023-02-26 08:06:18'),
(18, 'years_work_current_hotel', 'Total years at Current Hotel', 'Provide opportunities for career development within the organization', '2023-02-26 08:06:18'),
(19, 'number_of_years_current_role', 'Numbe of Years in Current Role', 'number_of_years_current_role measure', '2023-02-26 08:06:18'),
(20, 'department', 'Department', 'department measure', '2023-02-26 08:06:18'),
(21, 'last_promotion', 'Last Promotion', 'last_promotion measure', '2023-02-26 08:06:18'),
(22, 'hotel_performance_asses', 'Performance Assessment', 'Conduct annual performance reviews', '2023-02-26 08:06:18'),
(69, 'distance_from_home', 'Distance From Home', 'Distance From Home measure', '2023-03-21 05:19:41');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `first_name` varchar(80) NOT NULL,
  `last_name` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` text NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `first_name`, `last_name`, `email`, `password`, `created_at`, `updated_at`) VALUES
(1, 'Nathindu', 'Himansha', 'nathindu@gmail.com', 'pbkdf2:sha256:260000$hOgosxIGp5uZGaJ8$43d68a7e36600418188abaf0448958e98b9bc53e62afd3845c4420e43987b195', '2023-03-13 15:31:20', NULL),
(2, 'Nathindu', 'Himansha', 'nathindu123@gmail.com', 'pbkdf2:sha256:260000$wCQJiGm4Xl5jDu03$b3932f8f52e26c7b9948a1988da888412b595965e55addaab7c63f5a021da6f0', '2023-03-14 09:42:03', NULL),
(3, 'Nathindu', 'Himansha', 'nathindu12gg3@gmail.com', 'pbkdf2:sha256:260000$JUcfJHeduKeseAO4$bb220f5eff942ac594549d241ace12ac68209faddb9a5e7b1a07793bb5516c55', '2023-03-16 10:53:11', NULL),
(4, 'Nasthindu', 'Himansha', 'nathindu0012gg3@gmail.com', 'pbkdf2:sha256:260000$dRMTziKJ330i5kXI$bf93d5c1fc7f1a26a83be8c960fb3235024fb0d93a21ef6d623b86367c876a2f', '2023-03-16 10:55:14', NULL),
(5, 'Nirmani', 'Karagamapitiya', 'kamki@gmail.com', 'pbkdf2:sha256:260000$rivf41JBxMHcMDYH$1c9ba886f5a9622d4ff4c89aadaf54e3a9f8cfe47bb9123aa6805574636fad11', '2023-03-21 10:47:38', NULL),
(6, 'Kamal', 'Perera', 'kamal@gmail.com', 'pbkdf2:sha256:260000$IvHKLui6dJ2PrGSN$04b7abf0db7666b58ac79dc98a1314d81bd55c9b93aa36d9a37ff2565d2f9c87', '2023-03-26 19:22:51', NULL),
(7, 'Nirmani', 'Rox', 'nirmani@gmail.com', 'pbkdf2:sha256:260000$WDZfyZuu0NUu6Xu3$89c591e5bdac939f67e56136be98f1e7d330e2872f8e8e4f5538160a5f35ae53', '2023-03-26 19:22:51', NULL),
(8, 'Nasthindu', 'Himansha', 'nathindu00123gg3@gmail.com', 'pbkdf2:sha256:260000$e6liQEmZWg7lvWic$15868afe6ab836dd032cda1f3044218810f5efbb5d00050f867b7aa4a3b68352', '2023-03-29 19:04:37', NULL),
(9, 'Test', 'User', 'test@gmail.com', 'pbkdf2:sha256:260000$Ee9lVLh06DSBf0NY$1228a485ba9b50bec4cc98fc3b378f3528b7f5250cf9c51c4f2a4031e4858303', '2023-04-02 09:58:57', NULL),
(10, 'Hilton', '', 'hilton@gmail.com', 'pbkdf2:sha256:260000$YfCKfhwIyzEaTuke$fc652c976b866386e8ead713c0fbaf239a8d63be9d28b677d282eae43211fa37', '2023-04-02 16:25:21', NULL),
(11, 'Shagrila', '', 'shangrila@gmail.com', 'pbkdf2:sha256:260000$bP7v2d6aGUTP7E4c$872427d99d0d2ea6b33f70abeaf54c4d3377ff6dac0eed0a942a69c403457c90', '2023-04-02 18:04:53', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `department`
--
ALTER TABLE `department`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_department_id` (`fk_department_id`);

--
-- Indexes for table `prediction`
--
ALTER TABLE `prediction`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_id_emp` (`fk_emp_id`);

--
-- Indexes for table `prediction_factor_mapping`
--
ALTER TABLE `prediction_factor_mapping`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_prediction_id` (`fk_prediction_id`),
  ADD KEY `fk_factor_id` (`fk_factor_id`);

--
-- Indexes for table `turnover_factor`
--
ALTER TABLE `turnover_factor`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `department`
--
ALTER TABLE `department`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT for table `prediction`
--
ALTER TABLE `prediction`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `prediction_factor_mapping`
--
ALTER TABLE `prediction_factor_mapping`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=110;

--
-- AUTO_INCREMENT for table `turnover_factor`
--
ALTER TABLE `turnover_factor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=70;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `employee`
--
ALTER TABLE `employee`
  ADD CONSTRAINT `fk_department_id` FOREIGN KEY (`fk_department_id`) REFERENCES `department` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `prediction`
--
ALTER TABLE `prediction`
  ADD CONSTRAINT `fk_id_emp` FOREIGN KEY (`fk_emp_id`) REFERENCES `employee` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `prediction_factor_mapping`
--
ALTER TABLE `prediction_factor_mapping`
  ADD CONSTRAINT `fk_factor_id` FOREIGN KEY (`fk_factor_id`) REFERENCES `turnover_factor` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_prediction_id` FOREIGN KEY (`fk_prediction_id`) REFERENCES `prediction` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

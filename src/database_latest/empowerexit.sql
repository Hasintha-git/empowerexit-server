-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 23, 2024 at 07:49 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `empowerexit`
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
(37, 'emp_02', 'Amal Perera', 'Office Helper', 2, '123, colombo', '077123456', 'N/A', '2022-12-12', 'A', '', 1, '0.22832167832167832', '173', '2023-03-21 00:40:17', '2023-07-19 20:10:25'),
(38, 'emp_03', 'Kamla Peries', 'Maintenance Man', 1, '123, colombo', '077123456', 'N/A', '2022-12-12', 'A', '', 1, '0.5454545454545454', '3', '2023-03-21 00:40:50', '2023-06-01 21:53:00'),
(39, 'emp_04', 'Nirmala Peries', 'Security Guard', 5, '123, colombo', '077123456', 'N/A', '2022-12-12', 'A', '', 1, '0.5454545454545454', '3', '2023-03-21 00:41:29', '2023-06-01 21:47:27'),
(40, 'emp_05', 'Nikila Peries', 'Admin', 1, '123, colombo', '077123456', 'N/A', '2022-12-12', 'A', '', 1, '0.5454545454545454', '3', '2023-03-21 00:42:11', '2023-06-01 21:54:45'),
(45, 'emp_06', 'Aruna Pathirana', 'Engineer', 4, '123, perera mawatha', '0777777777', 'NA', '2020-10-12', 'A', '', 1, '0.5454545454545454', '1', '2023-03-23 02:58:45', '2023-06-01 21:48:50'),
(58, 'emp_07', 'Saman Silva', 'housekeeper', 1, 'qwe', '123', 'er', '2023-05-01', 'A', '', 1, '0.5045454545454545', '6', '2023-05-17 04:29:51', '2023-06-01 21:57:24'),
(59, 'emp_08', 'Peter Pen', 'Housekeeper', 3, '12/10', '0771234567', 'Mr. Brown', '2023-04-30', 'B', '', 1, '0.25862470862470865', '9', '2023-05-21 15:03:26', '2023-06-01 21:51:05'),
(60, 'emp_09', 'Kamala Perera', 'Housekeeper', 3, 'peace road, Colombo ', '0112345678', 'Mr. Brown', '2023-05-01', 'D', '', 1, '0.25862470862470865', '9', '2023-05-27 20:53:50', '2023-06-01 21:50:14'),
(61, 'emp_10', 'Brinda Mel', 'g', 1, 'qwwe', '1234564444', 'dsds', '2023-05-16', 'B', '', 1, '0.22832167832167832', '10', '2023-05-28 17:59:53', '2023-06-01 21:54:10'),
(70, 'emp_11', 'Peter', 'Housekeeper', 3, '12/Lane', '0771234567', 'Mr. Brown', '2023-06-01', 'B', '', 1, '0.25862470862470865', '171', '2023-06-02 11:14:56', '2023-06-02 11:16:14'),
(71, 'emp_12', 'Peter Ban', 'Housekeeper', 1, '24/1, wide lane', '0712345678', 'Ms. Pereira', '2023-04-04', 'B', '', 1, '0.4818181818181818', '189', '2023-08-08 21:22:38', '2023-08-08 21:50:42'),
(72, 'emp_13', 'Bill Shane', 'Waiter', 1, '1/4, Lane', '0123456789', 'Mr. Agath', '2023-01-04', 'D', '', 1, '0.45151515151515154', '189', '2023-08-08 21:56:00', '2023-08-08 21:59:46'),
(73, 'emp_14', 'Saman Silva', 'Kitchen helper', 1, '2/3, red street', '0123568790', 'Mr. Sarath', '2022-07-11', 'D', '', 1, '0.45909090909090905', '173', '2023-08-08 21:57:52', '2023-08-08 22:16:36'),
(74, 'emp_15', 'Piyal Zoysa', 'Waiter', 1, '3/5, peace lane', '0123456789', 'Mr. Brown', '2023-08-01', 'C', '', 1, '0.3909090909090909', '180', '2023-08-08 22:20:28', '2024-04-13 13:09:03'),
(75, '1620', 'hasintha', 'Waiter', 1, 'delgahawatta road, hokandara,', '0786833903', 'yasas', '2021-08-08', 'A', '', 1, '0.496969696969697', '185', '2024-04-15 14:24:08', '2024-04-15 14:26:01');

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
(31, 37, 1, '0.22832167832167832', 9, '2023-03-21 10:14:01', '2024-04-02 20:10:25'),
(32, 38, 1, '0.5454545454545454', 3, '2023-03-21 10:50:20', '2024-06-19 10:50:20'),
(33, 39, 1, '0.5454545454545454', 3, '2023-03-21 10:50:24', '2023-08-01 10:50:24'),
(34, 40, 1, '0.5454545454545454', 3, '2023-03-21 10:50:27', '2023-08-01 10:50:27'),
(37, 45, 1, '0.5454545454545454', 1, '2023-03-30 10:18:48', '2023-08-01 10:29:27'),
(43, 58, 1, '0.5045454545454545', 6, '2023-05-17 04:31:42', '2023-08-01 21:56:28'),
(44, 60, 1, '0.25862470862470865', 9, '2023-05-27 20:55:53', '2023-08-01 21:03:32'),
(45, 59, 1, '0.25862470862470865', 9, '2023-05-28 17:58:50', '2023-08-01 17:58:50'),
(46, 61, 1, '0.22832167832167832', 10, '2023-05-28 18:00:43', '2023-08-01 18:00:43'),
(54, 70, 1, '0.25862470862470865', 11, '2023-06-02 11:16:14', '2023-08-02 11:16:14'),
(55, 71, 1, '0.4818181818181818', 5, '2023-08-08 21:50:40', '2023-08-08 21:50:40'),
(56, 72, 1, '0.45151515151515154', 4, '2023-08-08 21:59:46', '2023-08-08 21:59:46'),
(57, 73, 1, '0.45909090909090905', 5, '2023-08-08 22:16:35', '2023-08-08 22:16:35'),
(58, 74, 1, '0.45151515151515154', 5, '2023-08-08 22:22:09', '2023-08-08 22:22:09'),
(59, 74, 1, '0.3909090909090909', 10, '2024-04-13 13:09:02', '2024-04-13 13:09:02'),
(60, 75, 1, '0.496969696969697', 5, '2024-04-15 14:26:01', '2024-04-15 14:26:01');

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
(81, 32, 22, '0.23822123975648948', '2023-03-21 10:50:20', '2024-04-09 10:50:20'),
(82, 32, 15, '0.008440542194866953', '2023-03-21 10:50:20', '2023-08-01 10:50:20'),
(83, 32, 69, '0.006169900767082142', '2023-03-21 10:50:20', '2023-08-01 10:50:20'),
(84, 33, 22, '0.23822123975648948', '2023-03-21 10:50:24', '2023-08-01 10:50:24'),
(85, 33, 15, '0.008440542194866953', '2023-03-21 10:50:24', '2023-08-01 10:50:24'),
(86, 33, 69, '0.00564707405604525', '2023-03-21 10:50:24', '2023-08-01 10:50:24'),
(87, 34, 22, '0.23822123975648948', '2023-03-21 10:50:27', '2023-08-01 10:50:27'),
(88, 34, 15, '0.008440542194866953', '2023-03-21 10:50:27', '2023-08-01 10:50:27'),
(89, 34, 69, '0.00564707405604525', '0000-00-00 00:00:00', '2024-03-12 10:50:27'),
(107, 37, 22, '0.23822123975648948', '2023-03-30 10:29:27', '2023-07-30 10:29:27'),
(108, 37, 15, '0.008440542194866953', '2023-03-30 10:29:27', '2023-07-30 10:29:27'),
(109, 37, 69, '0.006169900767082142', '2023-03-30 10:29:27', '2023-07-30 10:29:27'),
(159, 44, 21, '0.060207777913101654', '2023-05-27 21:03:32', '2023-08-01 21:03:32'),
(160, 44, 13, '0.034537623373634245', '2023-05-27 21:03:33', '2023-08-01 21:03:33'),
(161, 44, 6, '0.020695837012757925', '2023-05-27 21:03:33', '2023-08-01 21:03:33'),
(162, 45, 21, '0.060207777913101654', '2023-05-28 17:58:51', '2023-08-01 17:58:51'),
(163, 45, 13, '0.034537623373634245', '2023-05-28 17:58:51', '2023-08-01 17:58:51'),
(164, 45, 6, '0.020695837012757925', '0000-00-00 00:00:00', '2023-07-28 17:58:51'),
(165, 46, 21, '0.06609062278584453', '2023-05-28 18:00:43', '2023-07-28 18:00:43'),
(166, 46, 13, '0.0307596783066306', '2023-05-28 18:00:43', '2023-07-28 18:00:43'),
(167, 46, 6, '0.021329401135078863', '2023-05-28 18:00:43', '2023-07-28 18:00:43'),
(180, 43, 20, '0.10017798365716511', '2023-05-28 21:56:28', '2023-07-28 21:56:28'),
(181, 43, 21, '0.07430240462623615', '2023-05-28 21:56:28', '2023-07-28 21:56:28'),
(182, 43, 13, '0.03420105643242357', '0000-00-00 00:00:00', '2023-05-28 21:56:28'),
(195, 54, 21, '0.060207777913101654', '2023-06-02 11:16:14', '2023-06-02 11:16:14'),
(196, 54, 13, '0.034537623373634245', '2023-06-02 11:16:14', '2023-06-02 11:16:14'),
(197, 54, 6, '0.020695837012757925', '2023-06-02 11:16:14', '2023-06-02 11:16:14'),
(204, 31, 21, '0.06898855944250865', '2023-07-19 20:10:25', '2023-07-19 20:10:25'),
(205, 31, 13, '0.03009898607718585', '2023-07-19 20:10:25', '2023-07-19 20:10:25'),
(206, 31, 6, '0.023756560113063045', '2023-07-19 20:10:25', '2023-07-19 20:10:25'),
(207, 55, 20, '0.07022483486636036', '2023-08-08 21:50:42', '2023-08-08 21:50:42'),
(208, 55, 21, '0.06479357941761346', '2023-08-08 21:50:42', '2023-08-08 21:50:42'),
(209, 55, 2, '0.029831008576011515', '2023-08-08 21:50:42', '2023-08-08 21:50:42'),
(210, 56, 21, '0.0639706465365853', '2023-08-08 21:59:46', '2023-08-08 21:59:46'),
(211, 56, 20, '0.05695477069547986', '2023-08-08 21:59:46', '2023-08-08 21:59:46'),
(212, 56, 13, '0.03601720878400164', '2023-08-08 21:59:46', '2023-08-08 21:59:46'),
(213, 57, 21, '0.0663831952616388', '2023-08-08 22:16:36', '2023-08-08 22:16:36'),
(214, 57, 20, '0.06536729357704518', '2023-08-08 22:16:36', '2023-08-08 22:16:36'),
(215, 57, 13, '0.02970068116451877', '2023-08-08 22:16:36', '2023-08-08 22:16:36'),
(216, 58, 20, '0.08340529977841646', '2023-08-08 22:22:09', '2023-08-08 22:22:09'),
(217, 58, 21, '0.07267487573420434', '2023-08-08 22:22:09', '2023-08-08 22:22:09'),
(218, 58, 13, '0.02460067346499648', '2023-08-08 22:22:09', '2023-08-08 22:22:09'),
(219, 59, 21, '0.06553380966822386', '2024-04-13 13:09:03', '2024-04-13 13:09:03'),
(220, 59, 20, '0.040620456067047846', '2024-04-13 13:09:03', '2024-04-13 13:09:03'),
(221, 59, 13, '0.02917204097865007', '2024-04-13 13:09:03', '2024-04-13 13:09:03'),
(222, 60, 20, '0.07830036020920444', '2024-04-15 14:26:01', '2024-04-15 14:26:01'),
(223, 60, 21, '0.07080559318401701', '2024-04-15 14:26:01', '2024-04-15 14:26:01'),
(224, 60, 13, '0.036526531603336104', '2024-04-15 14:26:01', '2024-04-15 14:26:01');

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
(3, 'work_life_balance', 'Work Life Balance', 'Offer flexible work arrangements.', '2023-02-24 15:58:30'),
(4, 'status_and_recognition', 'Status and Recognition', 'Celebrate employee milestones. ', '2023-02-24 15:58:30'),
(5, 'salary', 'Salary', 'Provide performance-based pay increases.', '2023-02-24 15:58:30'),
(6, 'opportunities', 'Opportunities', 'Offer competitive compensation packages.', '2023-02-24 15:58:30'),
(7, 'workload', 'Workload', 'Provide resources to help employees manage their workload.', '2023-02-24 15:58:30'),
(8, 'work_environment', 'Work Environment', 'Foster a supportive work environment.', '2023-02-24 15:58:30'),
(9, 'training_and_development', 'Training and Development', 'Offer training and mentoring to employees.', '2023-02-24 15:58:30'),
(10, 'relationship_with_colleagues', 'Relationship with Colleagues', 'Foster a collaborative work culture.', '2023-02-24 15:58:30'),
(11, 'relationship_with_supervisor', 'Relationship with Supervisor', 'Encourage regular communication between employees and supervisors.', '2023-02-24 15:58:30'),
(12, 'job_satisfaction', 'Job Satisfaction', 'Conduct regular surveys to analyse employee job satisfaction', '2023-02-24 15:58:30'),
(13, 'age', 'Age', 'Offer opportunities for career advancement to help employee see a future with the IT. ', '2023-02-26 08:04:39'),
(14, 'gender', 'Gender', 'Ensure equal pay and refrain from gender discrimination.', '2023-02-26 08:05:32'),
(15, 'marital_status', 'Marital Status', 'Offer family-friendly benefits and support major life events.', '2023-02-26 08:06:18'),
(16, 'educational_status', 'Educational Status', 'Help employees develop new skills and advance their careers.', '2023-02-26 08:06:18'),
(17, 'total_years_industry', 'Total Years in Industry', 'Offer opportunities for career advancement.', '2023-02-26 08:06:18'),
(18, 'years_work_current_hotel', 'Total years at Current Hotel', 'Provide opportunities for career development within the organization', '2023-02-26 08:06:18'),
(19, 'number_of_years_current_role', 'Numbe of Years in Current Role', 'Offer opportunities for employees to grow in current role.', '2023-02-26 08:06:18'),
(20, 'department', 'Department', 'Foster teamwork and collaboration within the department.', '2023-02-26 08:06:18'),
(21, 'last_promotion', 'Last Promotion', 'Establish transparent promotion criteria.', '2023-02-26 08:06:18'),
(22, 'hotel_performance_asses', 'Performance Assessment', 'Conduct annual performance reviews', '2023-02-26 08:06:18'),
(69, 'distance_from_home', 'Distance From Home', 'Offer convenient commuting arrangements.', '2023-03-21 05:19:41');

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
(12, 'Nirmani', '', 'nirmani811@gmail.com', 'pbkdf2:sha256:260000$FhlClHeLjttP7HxO$25e15b86e0dbcffb5c57d3a596d30148d2de37b575f6bb3d2392b84827056c12', '2023-04-19 18:54:21', NULL),
(22, 'hotela', '', 'hotela@gmail.com', 'pbkdf2:sha256:260000$kBi2tuvEdvdTy2nf$6eeef07fc63c3d7b55a132ffaf9b346b89445b8e94f59460dcb9ffc7ae50a8f6', '2023-05-31 08:05:54', NULL),
(23, 'hotelb', '', 'hotelb@gmail.com', 'pbkdf2:sha256:260000$GMidYymKtgDk1LUp$b1f5a63dc817760bec0613f8575d983a7d7ece6b28c16a765c9b661591494316', '2023-05-31 08:05:54', NULL),
(24, 'hotelc', '', 'hotelc@gmail.com', 'pbkdf2:sha256:260000$3WFmiXSM4o96SXUW$0a6d6ac82f1b654da4cdec721f8ebc85e3fddef80146d834928410c80ea12fd1', '2023-05-31 08:05:54', NULL),
(25, 'hoteld', '', 'hoteld@gmail.com', 'pbkdf2:sha256:260000$AYo2wmGn685T2jn5$5b31faaa98e7a6df11d132d19b31e08e92ce520c2d52a7193609d43772acb34d', '2023-05-31 08:05:54', NULL),
(26, 'hotelc', '', 'hotel@gmail.com', 'pbkdf2:sha256:260000$FmKp6IJ9THu07i5k$a8da0bc7f328e0f0af528ea0e9a7044ce2f8ed5aa75e90ed1daa4988f5b19a46', '2023-05-31 08:05:54', NULL),
(27, 'hotel', '', 'hotelj@gmail.com', 'pbkdf2:sha256:260000$m6NXq8BX3rnizRMj$cd39e3ff3facfa6553fed3a242e316515324ed9ffab4dc6eb14352ed253dce8f', '2023-06-02 10:28:20', NULL),
(28, 'super', '', 'admin@gmail.com', 'pbkdf2:sha256:260000$VjZouvDVntPPr5ef$9e949495a33329a9374f3868b6f4dc6b206e7cfac4291b69bc8106a39ad15876', '2024-04-11 15:07:26', NULL),
(29, 'hasi', '', 'hasi@gmail.com', 'pbkdf2:sha256:260000$ohiqfcEVchjitVxT$bead551d7cbdfa10de281dcfcb52c83e0db68e6f51460b187c06fe99f4e958a8', '2024-04-17 17:00:16', NULL);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=76;

--
-- AUTO_INCREMENT for table `prediction`
--
ALTER TABLE `prediction`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `prediction_factor_mapping`
--
ALTER TABLE `prediction_factor_mapping`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=225;

--
-- AUTO_INCREMENT for table `turnover_factor`
--
ALTER TABLE `turnover_factor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=70;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

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

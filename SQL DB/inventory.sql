-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 07, 2024 at 06:41 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `inventory`
--

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `customer_name` varchar(20) DEFAULT NULL,
  `customer_contact` varchar(20) NOT NULL,
  `customer_email` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `organisation`
--

CREATE TABLE `organisation` (
  `organisation_id` int(11) NOT NULL,
  `organisation_name` varchar(20) DEFAULT NULL,
  `organisation_type` varchar(20) DEFAULT NULL,
  `organisation_location` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `organisation`
--

INSERT INTO `organisation` (`organisation_id`, `organisation_name`, `organisation_type`, `organisation_location`) VALUES
(1, 'Inventree Client', 'General Stores', 'Pune');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` varchar(13) NOT NULL,
  `product_manufacturer` varchar(30) DEFAULT NULL,
  `product_manufacturer_code` varchar(5) DEFAULT NULL,
  `product_category` varchar(20) DEFAULT NULL,
  `product_category_code` varchar(1) DEFAULT NULL,
  `product_name` varchar(30) DEFAULT NULL,
  `product_name_code` varchar(5) DEFAULT NULL,
  `product_price` float DEFAULT NULL,
  `product_measure` enum('unit','kg','liter','others') DEFAULT NULL,
  `product_size` varchar(15) DEFAULT NULL,
  `product_expiry` date DEFAULT NULL,
  `product_mfg` date DEFAULT NULL,
  `product_stock_quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `product_manufacturer`, `product_manufacturer_code`, `product_category`, `product_category_code`, `product_name`, `product_name_code`, `product_price`, `product_measure`, `product_size`, `product_expiry`, `product_mfg`, `product_stock_quantity`) VALUES
('9780201379624', '', '78020', '', '9', '', '37962', 0, '', 'Choose....', '0000-00-00', '0000-00-00', 10);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `user_username` varchar(30) DEFAULT NULL,
  `user_fullname` varchar(30) DEFAULT NULL,
  `user_password` varchar(16) DEFAULT NULL,
  `user_role` int(1) DEFAULT NULL,
  `user_contact` varchar(13) DEFAULT NULL,
  `user_email` varchar(30) DEFAULT NULL,
  `user_organisation_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `user_username`, `user_fullname`, `user_password`, `user_role`, `user_contact`, `user_email`, `user_organisation_id`) VALUES
(1, 'Mansur_khan', 'Mansur Khan', 'Pass@123', 2, '+917757963133', 'mansur_khan@inventree.com', 1),
(2, 'Aditya_Tongse', 'Aditya Tongse', 'Pass@123', 1, '+917350932355', 'aditya_tongse@inventree.com', 1),
(3, 'Shrikant_Dhobale', 'Shrikant Dhobale', 'Pass@123', 0, '+917219794805', 'shrikant_dhobale@inventree.com', 1),
(4, 'Vivek_Sharma', 'Vivek Sharma', 'Pass@123', 1, '+918305675632', 'vivek_sharma@inventree.com', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_contact`);

--
-- Indexes for table `organisation`
--
ALTER TABLE `organisation`
  ADD PRIMARY KEY (`organisation_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `organisation`
--
ALTER TABLE `organisation`
  MODIFY `organisation_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

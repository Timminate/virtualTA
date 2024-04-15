'use client'
// Page.js

import React from 'react';
import styles from './styles.module.css'; // Import your CSS module

const Page = () => {
  return (
    <div className={styles.container}>
      <div className={styles.profileCard}>
        {/* Your profile card content */}
        <img
          src="path/to/profile-image.jpg"
          alt="Profile"
          className={styles.profileImage}
        />
        <p className={styles.profileName}>Student name: John Doe</p>
        <p className={styles.profileName}>School email: j12345@utdallas.edu</p>
        <p className={styles.profileName}>Course Name: Data Structures and Algorithms</p>
        <p className={styles.profileName}>Course Number: CS 3345</p>
        <p className={styles.profileName}>Section Number: 005</p>
        <p className={styles.profileName}>Professor: Jane Doe</p>
      </div>
    </div>
  );
};

export default Page;

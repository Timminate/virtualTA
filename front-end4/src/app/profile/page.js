'use client'
import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';
import axios from 'axios';

const Page = () => {
  const [student, setStudent] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchStudentData = async () => {
      try {
        const response = await axios.get('/api/users/student');
        if (response.data && response.data.student) {
          const studentData = response.data.student;
          setStudent({
            firstName: studentData.firstName,
            lastName: studentData.lastName
            // Add other properties as needed
          });
        } else {
          setError('No student data available.');
        }
      } catch (error) {
        console.error(error);
        setError('An error occurred while fetching student data.');
      } finally {
        setLoading(false);
      }
    };
  
    fetchStudentData();
  }, []);

  return (
    <div className={styles.container}>
      <div className={styles.profileCard}>
        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p>{error}</p>
        ) : student ? (
          <>
            <img src="path/to/profile-image.jpg" alt="Profile" className={styles.profileImage} />
            <p className={styles.profileName}>Student name: {student.firstName} {student.lastName}</p>
            <p className={styles.profileName}>School email: j12345@utdallas.edu</p>
            <p className={styles.profileName}>Course Name: Data Structures and Algorithms</p>
            <p className={styles.profileName}>Course Number: CS 3345</p>
            <p className={styles.profileName}>Section Number: 005</p>
            <p className={styles.profileName}>Professor: Jane Doe</p>
          </>
        ) : (
          <p>No student data available.</p>
        )}
      </div>
    </div>
  );
};

export default Page;

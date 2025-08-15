import './index.css';
import { useEffect, useState } from 'react';
import axiosInstance from './utils/axios';
import LoginBlock from './components/LoginBlock';
import CourseBlock from './components/CourseBlock';
import axios from 'axios';
import { toast, ToastContainer } from 'react-toastify';
import CreateCourse from './components/CreateCourse';
import CreateVideo from './components/CreateVideo';
import VideoFetcher from './components/VideoFetcher';

function App() {
  const [itemId, setItemId] = useState('');
  const [curUser, setCurUser] = useState('');
  const [courseDetails, setCourseDetails] = useState(null);

  const [loginResult, setLoginResult] = useState('');
  useEffect(() => {
    const getCurUser = async () => {
      try {
        const getUser = await axiosInstance.get('/auth/me');
        setCurUser(getUser.data.data.user_id);
      } catch (err) {
        console.error(err);
        setCurUser('');
      }
    };
    getCurUser();
  }, []);

  const handleLogin = async (email, password) => {
    try {
      console.log('Logging in with:', { email, password });
      const response = await axiosInstance.post('/auth/login', {
        email,
        password,
      });
      setLoginResult('Login successful!');
      toast.success(
        `Logged in successfully with user ID: ${response.data.data.user_id}`
      );
      setCurUser(response.data.data.user_id);
    } catch (err) {
      console.error(err);
      setLoginResult('Login failed');
    }
  };

  const handleSignup = async (email, password) => {
    try {
      const response = await axiosInstance.post(
        'http://localhost:8000/auth/signup',
        {
          username: Math.random().toString(36).substring(7),
          email,
          password,
        }
      );
      setCurUser(response.data.data.user_id);
      toast.success(
        'Signed up successfully! With user ID: ' + response.data.data.user_id
      );
    } catch (err) {
      console.error(err);
      setLoginResult('Signup failed');
    }
  };
  const handleGetCourse = async (e, itemId) => {
    e.preventDefault();
    try {
      const response = await axiosInstance.get(`/courses/${itemId}`);
      console.log('Course details:', response.data);
      setCourseDetails(response.data.data);
      if (response.data.status === 'fail') {
        toast.error(response.data.message);
      }
    } catch (err) {
      console.error(err);
      toast.error('Failed to fetch course details');
      setCourseDetails(null);
    }
    setItemId('');
  };

  const handleCreateCourse = async (e, courseData) => {
    e.preventDefault();
    try {
      const response = await axiosInstance.post('/courses', courseData);
      console.log('Course created:', response.data);
      toast.success(
        'Course created successfully! with ID: ' + response.data.data.id
      );
    } catch (err) {
      console.error(err);
      toast.error(err?.response?.data?.detail || 'Failed to create course');
    }
  };

  const handleCreateVideo = async (e, videoData, setUploading) => {
    e.preventDefault();
    try {
      setUploading(true);
      const response = await axiosInstance.post('/courses/videos', videoData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      toast.success(
        'Video created successfully! with Asset ID: ' +
          response.data.data.asset_id
      );
    } catch (err) {
      console.error(err);
      toast.error(err?.response?.data?.detail || 'Failed to create video');
    } finally {
      setUploading(false);
    }
  };

  return (
    <>
      <div className="text-center">
        <h1 className="text-3xl font-bold text-blue-600 mb-4">API Test Page</h1>
        {curUser && <h1>Current user ID: {curUser}</h1>}
      </div>
      <div className="min-h-screen bg-gray-100 p-8 grid grid-cols-3 gap-8">
        {/* Login/Signup Block */}
        <LoginBlock
          handleLogin={handleLogin}
          handleSignup={handleSignup}
          loginResult={loginResult}
        />

        {/* create course block */}
        <CreateCourse handleCreateCourse={handleCreateCourse} />

        {/* create video block */}
        <CreateVideo handleCreateVideo={handleCreateVideo} />

        {/* ID Details Block */}
        <CourseBlock
          handleGetCourse={handleGetCourse}
          itemDetails={courseDetails}
        />

        {/* Video Preview by asset id */}
        <VideoFetcher />
        <ToastContainer />
      </div>
    </>
  );
}

export default App;

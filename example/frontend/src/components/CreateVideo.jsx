import React, { useState } from 'react';

function getMediaDuration(file) {
  return new Promise((resolve, reject) => {
    const video = document.createElement('video');
    video.preload = 'metadata';
    video.onloadedmetadata = () => {
      resolve(video.duration);
    };
    video.onerror = (e) => {
      reject(new Error('Error loading video metadata: ' + e.message));
    };
    video.src = URL.createObjectURL(file);
  });
}

const CreateVideo = ({ handleCreateVideo }) => {
  const [uploading, setUploading] = useState(false);
  const [videoData, setVideoData] = useState({
    title: '',
    description: '',
    course_id: '',
    duration: '',
    category: '',
    subcategory: '',
    file: null,
  });

  const handleChange = async (e) => {
    const { name, value, type, files } = e.target;
    if (type === 'file') {
      const duration = await getMediaDuration(files[0]);
      console.log('Video duration:', duration);
      setVideoData({ ...videoData, duration: duration, [name]: files[0] });
    } else {
      setVideoData({ ...videoData, [name]: value });
    }
  };

  return (
    <div>
      <div className="bg-white rounded shadow p-6 w-full max-w-md h-full items-center justify-center flex flex-col gap-4">
        <h2 className="text-xl font-semibold mb-2">Create Video</h2>
        <h4 className="text-gray-600">(Duration is set automatically)</h4>
        <p className="text-gray-600 mb-4 text-center">Make sure the video is .mp4. Currently the only supported extension by the streaming service free plan</p>
        <p className="text-gray-400 mb-4 text-center">
          Fill in the details below to create a new video linked to a course
        </p>
        <form
          className="flex flex-col gap-2"
          onSubmit={(e) => e.preventDefault()}
        >
          <input
            type="text"
            name="title"
            placeholder="Title"
            className="border rounded px-3 py-2 flex-1"
            value={videoData.title}
            onChange={handleChange}
          />
          <input
            type="text"
            name="description"
            placeholder="Description"
            className="border rounded px-3 py-2 flex-1"
            value={videoData.description}
            onChange={handleChange}
          />
          <input
            type="text"
            name="course_id"
            placeholder="Course ID"
            className="border rounded px-3 py-2 flex-1"
            value={videoData.course_id}
            onChange={handleChange}
          />
          <input
            type="file"
            name="file"
            accept="video/mp4"
            className="border rounded px-3 py-2 flex-1"
            onChange={handleChange}
          />
          <input
            type="text"
            name="category"
            placeholder="Category"
            className="border rounded px-3 py-2 flex-1"
            value={videoData.category}
            onChange={handleChange}
          />
          <input
            type="text"
            name="subcategory"
            placeholder="Subcategory"
            className="border rounded px-3 py-2 flex-1"
            value={videoData.subcategory}
            onChange={handleChange}
          />
          <button
            className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600 cursor-pointer transition-colors"
            type="button"
            disbabled={uploading}
            onClick={(e) => handleCreateVideo(e, videoData, setUploading)}
          >
            {uploading ? 'Uploading...' : 'Create Video'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreateVideo;

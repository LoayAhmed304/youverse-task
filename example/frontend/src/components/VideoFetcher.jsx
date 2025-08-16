import React, { useState, useRef, useEffect } from 'react';
import axiosInstance from '../utils/axios';
import { toast } from 'react-toastify';

const VideoFetcher = () => {
  const [assetId, setAssetId] = useState('');
  const [playbackId, setPlaybackId] = useState('');
  const playerRef = useRef(null);

  useEffect(() => {
    const script = document.createElement('script');
    script.src =
      'https://cdn.jsdelivr.net/npm/@mux/mux-player@2.4.0/dist/mux-player.min.js';
    script.async = true;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  useEffect(() => {
    if (playerRef.current && playbackId) {
      playerRef.current.setAttribute('playback-id', playbackId);
    }
  }, [playbackId]);

  const handleFetchVideo = async () => {
    if (!assetId.trim()) {
      alert('Please enter an Asset ID');
      return;
    }
    try {
      // Example API request — replace with your actual endpoint
      const res = await axiosInstance(`/courses/videos/${assetId}`);
      if (res.data?.status === 'fail') {
        toast.error(res.data.message || 'Failed to fetch video');
        return;
      }
      toast.success('Video fetched successfully!');

      setPlaybackId(res.data.data.video_details.playback_ids[0]); // Assuming API returns { playbackId: "xxx" }
    } catch (error) {
      console.error(error);
      toast.error('Failed to fetch video');
      setPlaybackId('');
    }
  };

  return (
    <div>
      <div className="bg-white h-full items-center justify-center rounded shadow p-6 w-200 flex flex-col gap-4">
        <h1 className="font-semibold text-xl">Video Preview</h1>
        <h4 className="text-gray-600">
          Displays the asset (video) playback streaming link from the streaming
          service
        </h4>
        <p className="text-gray-400 mb-2">
          Also must be enrolled or the owner of the course
        </p>

        <textarea
          rows={3}
          placeholder="Paste Asset ID here"
          value={assetId}
          onChange={(e) => setAssetId(e.target.value)}
          className="w-full mb-10 p-1 text-md border border-gray-300 rounded bg-white"
        />

        <button
          className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600 cursor-pointer transition-colors"
          type="button"
          onClick={handleFetchVideo}
        >
          Display Playback
        </button>

        {playbackId && (
          <mux-player
            ref={playerRef}
            className="w-full h-96"
            stream-type="on-demand"
            metadata-video-title="Fetched Video"
            metadata-viewer-user-id="test-user"
          ></mux-player>
        )}
      </div>
    </div>
  );
};

export default VideoFetcher;

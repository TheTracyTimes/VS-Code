import React, { useEffect, useState } from 'react';
import './DoveAnimation.css';

interface DoveAnimationProps {
  onComplete?: () => void;
}

const DoveAnimation: React.FC<DoveAnimationProps> = ({ onComplete }) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    // Auto-hide after 8 seconds
    const timer = setTimeout(() => {
      setIsVisible(false);
      onComplete?.();
    }, 8000);

    return () => clearTimeout(timer);
  }, [onComplete]);

  const handleDismiss = () => {
    setIsVisible(false);
    onComplete?.();
  };

  if (!isVisible) return null;

  return (
    <div className="dove-container" onClick={handleDismiss}>
      <div className="dove-wrapper">
        <svg
          className="dove"
          viewBox="0 0 200 200"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Dove body */}
          <ellipse cx="100" cy="100" rx="30" ry="40" fill="white" stroke="#ddd" strokeWidth="2" />

          {/* Dove head */}
          <circle cx="100" cy="75" r="18" fill="white" stroke="#ddd" strokeWidth="2" />

          {/* Beak */}
          <path d="M 110 75 L 120 75 L 115 78 Z" fill="#FFD700" />

          {/* Eye */}
          <circle cx="105" cy="72" r="3" fill="#333" />

          {/* Left wing (animated) */}
          <path
            className="wing-left"
            d="M 70 90 Q 40 80 30 70 Q 45 85 70 95 Z"
            fill="white"
            stroke="#ddd"
            strokeWidth="2"
          />

          {/* Right wing (animated) */}
          <path
            className="wing-right"
            d="M 130 90 Q 160 80 170 70 Q 155 85 130 95 Z"
            fill="white"
            stroke="#ddd"
            strokeWidth="2"
          />

          {/* Tail */}
          <path d="M 100 135 L 85 155 L 95 140 L 100 140 L 105 140 L 115 155 Z" fill="white" stroke="#ddd" strokeWidth="2" />

          {/* Olive branch in beak */}
          <g className="olive-branch">
            {/* Branch stem */}
            <path d="M 120 75 L 145 70" stroke="#8B4513" strokeWidth="2" fill="none" />

            {/* Leaves */}
            <ellipse cx="125" cy="68" rx="4" ry="6" fill="#90EE90" transform="rotate(-30 125 68)" />
            <ellipse cx="130" cy="69" rx="4" ry="6" fill="#90EE90" transform="rotate(30 130 69)" />
            <ellipse cx="135" cy="67" rx="4" ry="6" fill="#90EE90" transform="rotate(-30 135 67)" />
            <ellipse cx="140" cy="68" rx="4" ry="6" fill="#90EE90" transform="rotate(30 140 68)" />
            <ellipse cx="145" cy="66" rx="4" ry="6" fill="#90EE90" transform="rotate(-30 145 66)" />
          </g>
        </svg>

        <div className="dove-message">
          <h3>Welcome to Church Camp Analytics</h3>
          <p className="dove-subtitle">Peace be with you</p>
          <p className="dove-hint">Click anywhere to continue</p>
        </div>
      </div>
    </div>
  );
};

export default DoveAnimation;

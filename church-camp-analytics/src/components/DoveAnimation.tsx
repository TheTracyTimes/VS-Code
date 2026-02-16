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
        {/* Circular Logo Background */}
        <div className="logo-circle">
          <svg
            className="dove"
            viewBox="0 0 200 200"
            xmlns="http://www.w3.org/2000/svg"
          >
            {/* Dove body - simplified, clean white */}
            <ellipse cx="95" cy="105" rx="28" ry="35" fill="white" />

            {/* Dove head */}
            <circle cx="95" cy="78" r="16" fill="white" />

            {/* Beak - small yellow */}
            <path d="M 105 78 L 112 78 L 108 80 Z" fill="#FDB515" />

            {/* Eye */}
            <circle cx="100" cy="76" r="2.5" fill="#003DA5" />

            {/* Left wing - simplified smooth curve */}
            <path
              className="wing-left"
              d="M 70 95 Q 45 88 35 78 Q 42 85 50 90 Q 60 95 70 98 Z"
              fill="white"
            />

            {/* Right wing - simplified smooth curve */}
            <path
              className="wing-right"
              d="M 120 95 Q 145 88 155 78 Q 148 85 140 90 Q 130 95 120 98 Z"
              fill="white"
            />

            {/* Tail feathers - simplified */}
            <path
              d="M 95 135 L 85 150 L 90 138 L 95 138 L 100 138 L 105 150 Z"
              fill="white"
            />

            {/* Olive branch - cleaner design */}
            <g className="olive-branch">
              {/* Branch stem */}
              <path d="M 112 78 L 140 68" stroke="#6B8E23" strokeWidth="2.5" fill="none" />

              {/* Leaves - simplified oval shapes */}
              <ellipse cx="118" cy="73" rx="3.5" ry="5" fill="#90C050" transform="rotate(-35 118 73)" />
              <ellipse cx="122" cy="74" rx="3.5" ry="5" fill="#90C050" transform="rotate(25 122 74)" />
              <ellipse cx="128" cy="71" rx="3.5" ry="5" fill="#90C050" transform="rotate(-30 128 71)" />
              <ellipse cx="132" cy="72" rx="3.5" ry="5" fill="#90C050" transform="rotate(30 132 72)" />
              <ellipse cx="137" cy="69" rx="3.5" ry="5" fill="#90C050" transform="rotate(-25 137 69)" />
              <ellipse cx="141" cy="68" rx="3.5" ry="5" fill="#90C050" transform="rotate(20 141 68)" />
            </g>
          </svg>

          {/* Church name text around circle */}
          <div className="circle-text-top">ASSEMBLÉE ÉVANGÉLIQUE</div>
          <div className="circle-text-bottom">DE LAVAL</div>
        </div>

        <div className="dove-message">
          <h3>Bienvenue au Camp de l'Église</h3>
          <p className="dove-subtitle">La paix soit avec vous</p>
          <p className="dove-hint">Cliquez n'importe où pour continuer</p>
        </div>
      </div>
    </div>
  );
};

export default DoveAnimation;

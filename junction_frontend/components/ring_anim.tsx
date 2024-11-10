// First install dependencies:
// npm install lottie-react

import Lottie from 'lottie-react';
import ringAnimation from '../public/ring_anim.json'; // You'll need to create or download this

interface RingAnimationProps {
  size?: number;
  color?: string;
  speed?: number;
}

const LottieRingAnimation: React.FC<RingAnimationProps> = ({
  size = 200,
  color = '#3b82f6',
  speed = 1,
}) => {
  const defaultOptions = {
    loop: true,
    autoplay: true,
    animationData: ringAnimation,
    rendererSettings: {
      preserveAspectRatio: 'xMidYMid slice',
    },
  };

  return (
    <div style={{ width: size, height: size }}>
      <Lottie
        animationData={ringAnimation}
        loop={true}
        autoplay={true}
        style={{
          width: '100%',
          height: '100%',
          filter: `hue-rotate(${color})`,
        }}
      
      />
    </div>
  );
};

const audioRingStyles = {
  container: {
    position: 'relative' as const,
    width: '200px',
    height: '200px',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  },
  ring: {
    position: 'absolute' as const,
    width: '100%',
    height: '100%',
    border: '2px solid #3b82f6',
    borderRadius: '50%',
    animation: 'pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
  },
};

// Updated AudioRing component
const AudioRing = () => {
  return (
    <div style={audioRingStyles.container}>
      <LottieRingAnimation size={200} color="#3b82f6" speed={1} />
      {[...Array(3)].map((_, i) => (
        <div
          key={i}
          style={{
            ...audioRingStyles.ring,
            animationDelay: `${i * 0.3}s`,
          }}
        />
      ))}
    </div>
  );
};

export default AudioRing;
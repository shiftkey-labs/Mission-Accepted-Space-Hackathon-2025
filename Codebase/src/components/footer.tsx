import { type FC, useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import type { SatelliteData } from '@/types';

interface FooterProps {
	filteredSatellites: SatelliteData[];
}

const Footer: FC<FooterProps> = ({ filteredSatellites }) => {
	const [displayCount, setDisplayCount] = useState<number>(filteredSatellites.length);

	useEffect(() => {
		const start = displayCount;
		const end = filteredSatellites.length;
		const duration = 300;
		const startTime = performance.now();

		const animate = (now: number) => {
			const progress = Math.min((now - startTime) / duration, 1);
			const value = Math.floor(start + (end - start) * progress);

			setDisplayCount(value);

			if (progress < 1) {
				requestAnimationFrame(animate);
			}
		};

		requestAnimationFrame(animate);
	}, [filteredSatellites.length, displayCount]);

	return (
		<div className='z-10 absolute bottom-4 left-4 p-4 rounded-lg bg-neutral-200/20 backdrop-blur-md'>
			<motion.p key={displayCount} initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ duration: 0.3, ease: 'easeOut' }} className='font-mono text-sm text-white'>
				Satellites: {displayCount}
			</motion.p>

			<p className='hidden sm:block mt-1 font-mono text-sm text-neutral-200'>
				{/* Scroll to zoom • Drag to rotate • <strong>Hold SPACE</strong> to pause */}
				Scroll to zoom • Drag to rotate
			</p>

			<p className='block sm:hidden mt-1 font-mono text-sm text-neutral-200'>Pinch to zoom • Drag to rotate</p>
		</div>
	);
};

export { Footer };

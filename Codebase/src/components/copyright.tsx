const Copyright = () => {
	const currentYear = new Date().getFullYear();

	return (
		<div className='z-10 absolute bottom-4 right-4 hidden sm:block px-4 py-2 rounded-lg bg-neutral-200/20 backdrop-blur-md'>
			<p className='font-mono text-xs text-neutral-200'>
				Copyright &copy; <strong>Gianni • Gavin • Matthew</strong> {currentYear}
			</p>
		</div>
	);
};

export { Copyright };

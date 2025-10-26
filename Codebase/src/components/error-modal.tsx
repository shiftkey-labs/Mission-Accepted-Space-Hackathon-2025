import { X } from 'lucide-react';
import { type FC } from 'react';
import { type ErrorType } from '@/types';
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/react';

interface ErrorModalProps {
	error: ErrorType | null;
	open: boolean;
	onClose: () => void;
}

const ErrorModal: FC<ErrorModalProps> = ({ error, open, onClose }) => {
	return (
		<Dialog as='div' open={open} onClose={onClose} className='relative z-10 focus:outline-none'>
			<div className='fixed inset-0 z-10 w-screen overflow-y-auto'>
				<div className='p-4 flex min-h-full items-center justify-center'>
					<DialogPanel transition className='w-full max-w-md p-4 rounded-lg bg-neutral-200/20 backdrop-blur-md transition-all duration-300 ease-in-out data-closed:transform-[scale(95%)] data-closed:opacity-0'>
						<div className='w-full inline-flex items-center justify-between gap-4'>
							<DialogTitle as='h3' className='font-medium font-mono text-xl text-white'>
								{error?.title || 'Error'}
							</DialogTitle>

							<button type='button' onClick={onClose} className='select-none cursor-pointer p-2 flex items-center justify-center rounded-lg bg-neutral-300/30 hover:bg-neutral-300/50 text-white transition-all duration-300 ease-in-out'>
								<span className='sr-only'>Close</span>
								<X className='size-4' />
							</button>
						</div>

						<p className='mt-2 font-mono text-sm text-neutral-200 text-pretty'>{error?.message || 'An unknown error occurred.'}</p>
					</DialogPanel>
				</div>
			</div>
		</Dialog>
	);
};

export { ErrorModal };

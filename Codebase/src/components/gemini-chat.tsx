import { useEffect, useRef, useState } from 'react';
import { requestGeminiResponse, type GeminiChatMessage } from '@/utils';

type Message = {
	id: string;
	from: 'user' | 'gemini';
	text: string;
};

const GeminiChat = () => {
	// stages: 'open' (full), 'height' (short height, full width), 'square' (short height, narrow width)
	const [stage, setStage] = useState<'open' | 'height' | 'square'>('open');
	const timeoutRef = useRef<number | null>(null);
	const [input, setInput] = useState('');
	const [messages, setMessages] = useState<Message[]>([]);
	const [svgError, setSvgError] = useState(false);
	const scrollRef = useRef<HTMLDivElement | null>(null);
	const [isLoading, setIsLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);
	const abortControllerRef = useRef<AbortController | null>(null);

	// If you want to use a remote SVG for the collapsed Gemini icon, paste the URL here.
	// Example: const GEMINI_SVG_URL = 'https://example.com/gemini.svg';
	// Leave empty to use the fallback glyph.
	const GEMINI_SVG_URL = 'https://upload.wikimedia.org/wikipedia/commons/8/8f/Google-gemini-icon.svg';
	const SYSTEM_PROMPT =
		'You are Gemini, a friendly flight dynamics specialist helping people explore Canadian spacecraft currently in orbit. Focus on the satellites shown in the app, teach interesting facts, and help observers understand what to look for in the night sky. Answer concisely unless more detail is requested. Do not attempt to format or embolden things because it will not render properly.';

	useEffect(() => {
		if (scrollRef.current) {
			scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
		}
	}, [messages, stage]);

	const send = async () => {
		if (isLoading) return;

		const trimmedInput = input.trim();
		if (!trimmedInput) return;

		const userMsg: Message = { id: String(Date.now()), from: 'user', text: input };
		setMessages((prev) => [...prev, userMsg]);
		setInput('');
		setError(null);

		if (abortControllerRef.current) {
			abortControllerRef.current.abort();
		}
		const controller = new AbortController();
		abortControllerRef.current = controller;
		setIsLoading(true);

		try {
			const geminiHistory: GeminiChatMessage[] = [...messages, userMsg].slice(-10).map((msg) => ({
				role: msg.from === 'user' ? 'user' : 'model',
				text: msg.text,
			}));

			const replyText = await requestGeminiResponse(geminiHistory, {
				systemPrompt: SYSTEM_PROMPT,
				signal: controller.signal,
			});

			const reply: Message = { id: String(Date.now() + 1), from: 'gemini', text: replyText };
			setMessages((prev) => [...prev, reply]);
		} catch (err) {
			if ((err as Error)?.name === 'AbortError') {
				return;
			}
			const fallback = err instanceof Error ? err.message : 'Gemini is unavailable. Please try again.';
			setError(fallback);
			const reply: Message = { id: String(Date.now() + 2), from: 'gemini', text: fallback };
			setMessages((prev) => [...prev, reply]);
		} finally {
			setIsLoading(false);
			abortControllerRef.current = null;
		}
	};

	// Timing for the animations (ms). Keep slightly longer than Tailwind duration-150 (150ms)
	const HEIGHT_MS = 180;
	const WIDTH_MS = 180;

	useEffect(() => {
		return () => {
			if (timeoutRef.current) window.clearTimeout(timeoutRef.current);
			if (abortControllerRef.current) abortControllerRef.current.abort();
		};
	}, []);

	const toggleCollapse = () => {
		if (stage === 'open') {
			// Close: shrink height first, then width -> square
			setStage('height');
			timeoutRef.current = window.setTimeout(() => setStage('square'), HEIGHT_MS);
		} else if (stage === 'square') {
			// Open: expand width first (go to height stage which has full width), then expand height
			setStage('height');
			timeoutRef.current = window.setTimeout(() => setStage('open'), WIDTH_MS);
		} else if (stage === 'height') {
			// If in middle, toggle to square for quick collapse
			setStage('square');
		}
	};

	return (
		<div>
			{/* Desktop: fixed left panel anchored to bottom. Collapses bottom-up then right-to-left to become a square. */}
			<div className={`fixed left-4 top-66 z-40 hidden md:flex flex-col transition-all duration-150 ${stage === 'open' ? 'h-130' : 'h-12'} ${stage === 'square' ? 'w-12' : 'w-80'}`}>
				<div className={`flex flex-col h-full bg-neutral-200/10 backdrop-blur rounded-lg shadow-md overflow-hidden border border-neutral-700`}>
					{/* Header */}
					<div className='flex items-center justify-between px-2 py-2 bg-neutral-200/6'>
						<div className='flex items-center gap-2'>
							<div className='h-7 w-7 bg-neutral-300/20 rounded-md flex items-center justify-center text-white font-mono'>
								{stage === 'square' && GEMINI_SVG_URL && !svgError ? (
									<img src={GEMINI_SVG_URL} alt='Gemini' className='h-4 w-4 object-contain' onError={() => setSvgError(true)} />
								) : stage === 'square' ? (
									/* Use the Gemini astrological glyph as the icon when fully collapsed or if SVG fails */
									<span className='text-sm'>♊</span>
								) : (
									'G'
								)}
							</div>
							{stage === 'open' && <div className='text-xs font-mono text-neutral-100'>Gemini</div>}
						</div>
						<div className='flex items-center gap-1'>
							<button className='text-neutral-300 text-xs px-2 py-1 rounded hover:bg-neutral-700/30' onClick={toggleCollapse} title={stage === 'open' ? 'Collapse' : 'Open'}>
								{/* SVG chevron */}
								<svg className={`w-3 h-3 transform transition-transform ${stage === 'open' ? 'rotate-180' : ''}`} viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'>
									<path d='M6 9l6 6 6-6' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' />
								</svg>
							</button>
							{isLoading && stage === 'open' && <span className='text-xs text-neutral-300 font-mono'>...</span>}
						</div>
					</div>

					{/* Messages - hide when collapsed (height small) */}
					<div ref={scrollRef} className={`flex-1 px-2 overflow-y-auto gemini-messages transition-opacity duration-150 ${stage === 'open' ? 'py-2 opacity-100' : 'py-0 opacity-0 pointer-events-none'}`}>
						{messages.length === 0 && stage === 'open' && <div className='text-neutral-400 text-xs font-mono'>Ask Gemini about satellites or the night sky.</div>}

						{messages.map((m) => (
							<div key={m.id} className={`mb-2 flex ${m.from === 'user' ? 'justify-end' : 'justify-start'}`}>
								<div className={`max-w-[80%] px-2 py-1 rounded-md text-xs font-mono break-words ${m.from === 'user' ? 'bg-neutral-700 text-white' : 'bg-neutral-700/50 text-neutral-100'}`} style={{ whiteSpace: 'break-spaces' }}>
									{m.text}
								</div>
							</div>
						))}
						{isLoading && stage === 'open' && (
							<div className='mb-2 flex justify-start' aria-live='polite'>
								<div className='max-w-[80%] px-2 py-1 rounded-md bg-neutral-700/40 text-xs font-mono text-neutral-100'>
									<div className='gemini-typing-indicator' aria-hidden='true'>
										<span className='gemini-typing-indicator__dot' />
										<span className='gemini-typing-indicator__dot' />
										<span className='gemini-typing-indicator__dot' />
									</div>
									<span className='sr-only'>Gemini is typing</span>
								</div>
							</div>
						)}
					</div>

					{/* Input - hide when collapsed */}
					<div className={`px-2 bg-neutral-200/6 transition-opacity duration-150 ${stage === 'open' ? 'py-2 opacity-100' : 'py-0 opacity-0 pointer-events-none'}`}>
						{stage === 'open' ? (
							<>
								<div className='flex gap-2'>
									<input
										value={input}
										onChange={(e) => setInput(e.target.value)}
										onKeyDown={(e) => {
											if (e.key === 'Enter') send();
										}}
										placeholder='Message Gemini...'
										className='flex-1 bg-neutral-700/30 text-neutral-100 placeholder-neutral-400 px-2 py-1 rounded-md outline-none text-xs font-mono disabled:opacity-60'
										disabled={isLoading}
									/>
									<button onClick={send} disabled={!input.trim() || isLoading} className='px-2 py-1 bg-neutral-600 hover:bg-neutral-500 disabled:bg-neutral-700/50 disabled:cursor-not-allowed text-white rounded-md text-xs font-mono'>
										Send
									</button>
								</div>
								{error && <div className='mt-1 text-[10px] text-red-200 font-mono'>{error}</div>}
							</>
						) : null}
					</div>
				</div>

				<span className='sr-only' aria-live='polite'>
					{isLoading ? 'Gemini is generating a reply' : ''}
				</span>
			</div>
		</div>
	);
};

export { GeminiChat };

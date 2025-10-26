export type GeminiChatMessage = {
	role: 'user' | 'model';
	text: string;
};

type GeminiPart = {
	text?: string;
};

type GeminiContent = {
	role: 'user' | 'model';
	parts: GeminiPart[];
};

type GeminiCandidate = {
	content?: GeminiContent;
	finishReason?: string;
};

type GeminiResponse = {
	candidates?: GeminiCandidate[];
};

const GEMINI_API_BASE = 'https://generativelanguage.googleapis.com/v1beta';
const DEFAULT_MODEL = import.meta.env.VITE_GEMINI_MODEL ?? 'gemini-1.5-flash-latest';

const buildContents = (messages: GeminiChatMessage[], systemPrompt?: string): GeminiContent[] => {
	const contents: GeminiContent[] = [];

	if (systemPrompt?.trim()) {
		contents.push({
			role: 'user',
			parts: [{ text: systemPrompt.trim() }],
		});
	}

	messages.forEach((message) => {
		contents.push({
			role: message.role,
			parts: [{ text: message.text }],
		});
	});

	return contents;
};

const extractResponseText = (payload: GeminiResponse): string => {
	const parts = payload.candidates?.[0]?.content?.parts ?? [];
	const text = parts
		.map((part) => part.text?.trim())
		.filter(Boolean)
		.join('\n')
		.trim();

	if (!text) {
		throw new Error('Gemini returned an empty response. Please try again.');
	}

	return text;
};

export type GeminiCompletionOptions = {
	systemPrompt?: string;
	signal?: AbortSignal;
	model?: string;
};

export const requestGeminiResponse = async (messages: GeminiChatMessage[], options: GeminiCompletionOptions = {}) => {
	const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
	if (!apiKey) {
		throw new Error('Missing Gemini API key. Set VITE_GEMINI_API_KEY in your environment.');
	}

	const contents = buildContents(messages, options.systemPrompt);
	const endpoint = `${GEMINI_API_BASE}/models/${options.model ?? DEFAULT_MODEL}:generateContent?key=${apiKey}`;

	const response = await fetch(endpoint, {
		method: 'POST',
		signal: options.signal,
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
			contents,
		}),
	});

	if (!response.ok) {
		let message = `Gemini request failed (${response.status})`;
		try {
			const errorPayload = await response.json();
			message = errorPayload.error?.message ?? message;
		} catch {
			// Ignore JSON parse errors and fall back to status text.
		}
		throw new Error(message);
	}

	const data: GeminiResponse = await response.json();

	return extractResponseText(data);
};

// @ts-nocheck
import { createGoogleGenerativeAI } from '@ai-sdk/google'; // Import the creator function
import { streamText } from 'ai'; 
import { Index } from '@upstash/vector';
import { env } from '$env/dynamic/private';

const index = new Index({
  url: env.UPSTASH_VECTOR_REST_URL,
  token: env.UPSTASH_VECTOR_REST_TOKEN,
});

// Explicitly pass the key from SvelteKit to the Google SDK
const google = createGoogleGenerativeAI({
  apiKey: env.GOOGLE_GENERATIVE_AI_API_KEY,
});

export async function POST({ request }) {
  const { messages } = await request.json();

  const safeMessages = messages.map(msg => {
    let textContent = "";
    if (typeof msg.content === 'string' && msg.content.length > 0) {
      textContent = msg.content;
    } else if (msg.parts && Array.isArray(msg.parts)) {
      textContent = msg.parts.map(p => p.text || '').join('');
    }
    return { role: msg.role, content: textContent };
  });

  const lastUserMessage = safeMessages[safeMessages.length - 1]?.content.toLowerCase() || "";
  
  let dynamicSystemPrompt = 'You are the ShutUP Forwarder AI agent. You help manage logistics.';

  if (lastUserMessage.includes('vector') || lastUserMessage.includes('database') || lastUserMessage.includes('test')) {
      console.log("⚡ BYPASS ACTIVATED: Fetching Upstash manually before calling AI...");
      
      try {
          const data = await index.fetch(['test-job-uuid-12345']);
          if (data && data.length > 0) {
              dynamicSystemPrompt += `\n\nSYSTEM UPDATE: You just checked the database for the user. You found the mock vector! The ID is ${data[0]?.id}. Tell the user this exact ID immediately.`;
          } else {
              dynamicSystemPrompt += `\n\nSYSTEM UPDATE: You just checked the database. You could not find the test vector.`;
          }
      } catch (error) {
          console.error("Upstash Error:", error);
          dynamicSystemPrompt += `\n\nSYSTEM UPDATE: The database connection failed.`;
      }
  }

  const result = streamText({
    model: google('gemini-2.5-flash'), // Updated to an active general availability model
    system: dynamicSystemPrompt,
    messages: safeMessages,
  });

  if (typeof result.toUIMessageStreamResponse === 'function') {
      return result.toUIMessageStreamResponse();
  } else if (typeof result.toDataStreamResponse === 'function') {
      return result.toDataStreamResponse();
  } else {
      return result.toTextStreamResponse();
  }
}
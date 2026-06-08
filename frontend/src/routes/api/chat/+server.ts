// @ts-nocheck
import { createGoogleGenerativeAI } from '@ai-sdk/google'; 
import { streamText } from 'ai'; 
import { env } from '$env/dynamic/private';
import { PrismaClient } from '@prisma/client'; // Import the JS Prisma Client

// Initialize the Prisma Client to connect to Neon
const prisma = new PrismaClient();

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
      console.log("⚡ BYPASS ACTIVATED: Fetching from Neon DB manually before calling AI...");
      
      try {
          // Replaced Upstash fetch with a Prisma raw query to Neon
          // Fetching a single job just to verify the database connection works
          const data = await prisma.$queryRaw`SELECT id FROM "Job" LIMIT 1`;
          
          if (data && data.length > 0) {
              dynamicSystemPrompt += `\n\nSYSTEM UPDATE: You just checked the Neon database for the user. You successfully connected! A sample Job ID is ${data[0].id}. Tell the user this exact ID immediately to prove the connection works.`;
          } else {
              dynamicSystemPrompt += `\n\nSYSTEM UPDATE: You just checked the Neon database. The connection works, but the Job table is currently empty.`;
          }
      } catch (error) {
          console.error("Neon DB Error:", error);
          dynamicSystemPrompt += `\n\nSYSTEM UPDATE: The Neon database connection failed.`;
      }
  }

  const result = streamText({
    model: google('gemini-2.5-flash'), 
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
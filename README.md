Veritas AI(Version 1) - Advanced Text Analysis Tool
Veritas AI is a modern, web-based application designed for journalists, researchers, and discerning readers to analyze text for misinformation, bias, and rhetorical manipulation. It leverages the power of a Large Language Model (LLM) to provide a nuanced, data-driven breakdown of content in a sleek, professional user interface.

Features
Sophisticated Dark Mode UI: A professional and visually appealing interface designed for focused work.

LLM-Powered Analysis: Utilizes Google's Gemini model for deep, contextual understanding of text.

Comprehensive Credibility Score: An at-a-glance percentage score (0-100%) indicating the likely credibility of the provided text.

Detailed Linguistic Breakdown:

Bias Meter: A visual gauge showing where the text falls on the political spectrum (Left, Center, Right) or if it contains other forms of bias.

Tone Analysis: Identifies the tone of the text (e.g., Objective, Sensationalist, Formal).

Persuasive Techniques: Flags the use of rhetorical and manipulative techniques like "Appeal to Emotion," "Loaded Language," etc.

Key Claims Deconstruction: The AI identifies the main claims within the text and provides a brief, neutral assessment of each.

AI-Generated Summary: A concise summary of the AI's overall findings.

Single-File Application: The entire application is self-contained in a single HTML file, making it highly portable and easy to run.

How It Works
Veritas AI does not use a traditional, custom-trained machine learning model. Instead, it functions by sending the user-provided text to a powerful, general-purpose Large Language Model (Google's Gemini) via an API call.

The core of the application's logic lies in the System Prompt. This is a carefully engineered set of instructions that tells the LLM how to behave and what to do. The prompt commands the AI to:

Act as an expert analyst specializing in media bias and misinformation.

Analyze the text for specific criteria (credibility, claims, bias, tone).

Return its findings exclusively in a structured JSON format.

This method allows for complex, nuanced analysis without the need for building and maintaining a dedicated model. The backend logic in the browser then parses this JSON response and populates the data visualizations in the user interface.

Technology Stack
This is a frontend-only application with direct calls to the LLM API.

HTML5: For the core structure of the application.

Tailwind CSS: For the modern, responsive, and utility-first styling.

Vanilla JavaScript (ES6+): For all client-side logic, including API calls and DOM manipulation.

Google Gemini API: The Large Language Model that performs the text analysis.

Setup and Usage
Because Veritas AI is a single, self-contained file, there is no complex setup required.

Download the File: Save the veritas_ai.html file to your local machine.

Open in Browser: Open the file directly in any modern web browser (like Chrome, Firefox, or Edge).

The application is now ready to use. Simply paste the text you wish to analyze into the input box and click the "Analyze" button.

Note: The application relies on an API call to Google's Generative Language services. The API key is handled by the execution environment and is not hardcoded in the file.

Project Purpose
This tool was created to demonstrate how modern LLMs can be used for sophisticated text analysis tasks that go beyond simple true/false classifications. It is intended as a professional tool to aid in the critical evaluation of information by highlighting potential areas of concern in a piece of text.

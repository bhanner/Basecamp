# The Amazing Chat-o-tron 5000 (Credit to GianPiero Bresolin)

This is a chat application built with React and integrated with Azure OpenAI GPT-4o.

## Project Structure

```workspace
react-chat-app
├── public
│   ├── index.html
│   └── favicon.ico
├── src
│   ├── components
│   │   ├── ChatBox.tsx
│   │   ├── Message.tsx
│   │   ├── NamePrompt.tsx
│   │   └── index.ts
│   ├── services
│   │   └── openaiService.ts
│   ├── styles
│   │   ├── App.css
│   │   ├── ChatBox.css
│   │   ├── Message.css
│   ├── App.tsx
│   ├── index.tsx
│   └── react-app-env.d.ts
├── .eslintrc.json
├── .prettierrc
├── package.json
├── tsconfig.json
└── README.md
```

## File Descriptions

- `public/index.html`: HTML template for the React app.
- `public/favicon.ico`: Favicon for the React app.
- `src/components/ChatBox.tsx`: React component for the chat box UI.
- `src/components/Message.tsx`: React component for a single chat message.
- `src/components/NamePrompt.tsx`: React component for a single chat message.
- `src/components/index.ts`: Exports all components from the `components` directory.
- `src/services/openaiService.ts`: Service for making API calls to OpenAI GPT-4.
- `src/styles/App.css`: CSS styles for the `App` component.
- `src/App.tsx`: Main component of the React app.
- `src/index.tsx`: Entry point of the React app.
- `src/react-app-env.d.ts`: Declaration file for TypeScript.
- `.eslintrc.json`: ESLint configuration file.
- `.prettierrc`: Prettier configuration file.
- `tsconfig.json`: TypeScript configuration file.
- `package.json`: npm configuration file.
- `README.md`: Documentation for the project.

## Getting Started

1. Clone the repository.
1. Install the dependencies using `npm install`.
    - If you have conflicts, I found installing and using `pnpm` work for me
1. Create a file in the root of the workspace called .env to store your API Key:

```.env
REACT_APP_AZURE_OPENAI_API_KEY={YOUR_AZURE_OPENAI_API_LEY}
REACT_APP_AZURE_OPENAI_ENDPOINT={YOUR_AZURE_OPENAI_ENDPOINT}
```

1. Start the development server using `npm start`.

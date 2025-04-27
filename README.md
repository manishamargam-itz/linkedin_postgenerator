# LinkedIn Post Generator

An AI-powered LinkedIn post generator that helps create professional and engaging posts using Groq's LLM.

## Features

- 🤖 AI-powered post generation
- 📝 Customizable templates
- 📚 Post history management
- ✏️ Real-time editing
- 🎨 Template categories
- ⚙️ User preferences
- 📊 Character count tracking
- #️⃣ Hashtag suggestions

## Tech Stack

- **Backend**: Python
- **Frontend**: Streamlit
- **Database**: SQLite
- **AI/ML**: Groq LLM (llama3-8b-8192)
- **Libraries**: langchain-groq, streamlit

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/linkedin-post-generator.git
cd linkedin-post-generator
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your Groq API key:

```
GROQ_API_KEY=your_api_key_here
```

## Usage

1. Start the application:

```bash
streamlit run main.py
```

2. Open your browser and go to `http://localhost:8502`

3. Use the interface to:
   - Generate new posts
   - Create and manage templates
   - View post history
   - Edit existing posts
   - Customize settings

## Project Structure

```
linkedin-post-generator/
├── main.py              # Main application file
├── db_helper.py         # Database operations
├── llm_helper.py        # LLM integration
├── post_generator.py    # Post generation logic
├── few_shot.py          # Few-shot learning examples
├── requirements.txt     # Project dependencies
├── .env                 # Environment variables
└── README.md           # Project documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Groq for providing the LLM service
- Streamlit for the web framework
- All contributors who helped improve this project

## Deployment

### Local Deployment

1. Follow the installation instructions above
2. Start the application:
   ```bash
   streamlit run main.py
   ```
3. Access the application at `http://localhost:8502`

### Cloud Deployment

#### Option 1: Streamlit Cloud (Recommended)

1. Create a free account at [Streamlit Cloud](https://streamlit.io/cloud)
2. Connect your GitHub repository
3. Configure the following environment variables in Streamlit Cloud:
   - `GROQ_API_KEY`: Your Groq API key
4. Deploy the application

#### Option 2: Heroku

1. Install the Heroku CLI
2. Create a `Procfile` in your project root:
   ```
   web: streamlit run main.py --server.port $PORT
   ```
3. Create a `setup.sh` file:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```
4. Deploy to Heroku:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

#### Option 3: Docker

1. Create a `Dockerfile`:

   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8502
   CMD ["streamlit", "run", "main.py"]
   ```

2. Build and run the container:
   ```bash
   docker build -t linkedin-post-generator .
   docker run -p 8502:8502 -e GROQ_API_KEY=your_api_key linkedin-post-generator
   ```

### Environment Variables

For all deployment methods, ensure you have the following environment variables set:

- `GROQ_API_KEY`: Your Groq API key
- `STREAMLIT_SERVER_PORT`: Port number (default: 8502)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: 0.0.0.0)

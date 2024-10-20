from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, LLMChain
from langchain_chroma import Chroma
from dotenv import load_dotenv


load_dotenv()


class ChatBot:
    #Load the models
    def __init__(self, pdf_path):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro")
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.pdf_path = pdf_path

    def load_pdf(self):
        persist_directory = "./chroma_db"
        #Load the PDF and create chunks
        loader = PyPDFLoader(self.pdf_path)
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
        pages = loader.load_and_split(text_splitter)

        #Turn the chunks into embeddings and store them in Chroma
        vectordb=Chroma.from_documents(pages,self.embeddings, persist_directory=persist_directory)

        #Configure Chroma as a retriever with top_k=1
        self.retriever = vectordb.as_retriever(search_kwargs={"k": 5})


    def summarize(self):
        summarize_template="""
        You are a helpful AI assistant.
        The provided context contains emotions of user in a conversation. Analyse the moods of the user and provide a detailed summary of it. Include moods of each message in the context and then describe how how the mood has changed from first to last message.
        context: {context}
        input: {input}
        answer:
        Mood of First message:
        Mood of second message:
        and so on for all the messages possible.
        Summary of the change of moods over time:
        """

        self.load_pdf()
        self.create_chain(summarize_template)
        response = self.retrieval_chain.invoke({'input':'Can you analyse the mood and share how it has changed over time?'})
        return response['answer']


    def getlinks(self, summary=None):
        if not summary:
            summary = self.summarize()
        template = """Based on the summary of the conversation:
            {summary}
            Please provide a few helpful website links from the web for the user to feel more engaged and involved. If any mental health issue is discussed include reliable documentation from the web"""
        prompt = PromptTemplate(
            input_variables=["summary"],
            template=template,
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        # response = self.retrieval_chain.invoke({'input':'Can you provide some helpful links to uplift the user?'})
        response = chain.run(summary=summary)
        return response


    def create_chain(self, template):
        
        prompt = PromptTemplate.from_template(template)
        self.combine_docs_chain = create_stuff_documents_chain(self.llm, prompt)
        self.retrieval_chain = create_retrieval_chain(self.retriever, self.combine_docs_chain)
        # st.session_state['chain'] = self.retrieval_chain

    def ask_anything_continuous(self):

        self.load_pdf()

        template = """
        You are a helpful AI assistant.
        The provided context contains emotions of user in a conversation. Analyse it to provide details.
        context: {context}
        input: {input}
        answer:
        """
        self.create_chain(template)
        while True:

            i = input("Ask a question\n")
            response= self.retrieval_chain.invoke({"input":i})
            print(response["answer"])

    def ask_anything(self, input):
        template = """
            You are a helpful AI assistant.
            The provided context contains emotions of user in a conversation. Analyse it to provide details.
            context: {context}
            input: {input}
            answer:
            """
        self.create_chain(template)
        # print(self.retrieval_chain)
        response = self.retrieval_chain.invoke({'input':input})
        return response['answer']



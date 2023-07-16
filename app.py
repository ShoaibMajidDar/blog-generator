import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import  LLMChain
from langchain.llms import OpenAI
import os


OPENAI_API_KEY = st.text_input(":blue[Enter Your OPENAI API-KEY :]", 
                placeholder="Paste your OpenAI API key here (sk-...)",
                type="password",
                )
if OPENAI_API_KEY:
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

    llmgptt00 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, max_tokens=3000, max_retries=20)
    llmgptt03 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3, max_tokens=3000, max_retries=20)



    topics_template = PromptTemplate(
        input_variables = ['topic'],
        template = 'As an experienced blogger and technical writer,write 8 sub-topics name that should be included in a blog about the topic {topic} with the 8th sub topic as conclusion'
    )
    topics_chain = LLMChain(llm= llmgptt00, prompt=topics_template, verbose = True, )


    topic_writing_template = PromptTemplate(
        input_variables = ['topic', 'blog'],
        template = "write one or two paragraphs about the topic: {topic}, which is a sub-topic in the blog: {blog} "
    )
    topic_writing_chain = LLMChain(llm= llmgptt03, prompt=topic_writing_template, verbose = True , output_key='topics')


    blog_name = st.text_input(":blue[Enter Blog's name]", 
                    placeholder="",
                    type="default",
                    )
    
    with st.spinner('Wait for it...'):
        if blog_name:
            topics = ''
            topics = topics_chain(blog_name)
            topics = topics["text"].split('\n')
            complete_blog = ""
            for topic in topics:
                seg_blog = topic_writing_chain.run(topic = topic, blog = blog_name)
                topic = ' '.join(topic.split()[1:])
                complete_blog = complete_blog + '**' +topic.upper() + '**' + '''  \n''' + seg_blog + '''  \n''' + '''  \n'''
            st.write(complete_blog)
        st.success('')
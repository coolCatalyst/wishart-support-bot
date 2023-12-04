import React, { useEffect, useState, useRef } from "react";
import { postMessage, getData, leadCheck, removeData } from "../../../components/API";
import { useRouter } from "next/router";
import { autoResize } from "../../../components/utils";
import { LeadComponent } from "../../../components/LeadComponent";
import { Footer } from "../../../components/Sections/Footer";
import { Header } from "../../../components/Sections/Header";
import { WelcomeComponent } from "../../../components/Sections/Welcome";
import { DotLoading } from "../../../components/Styles";
import { MainComponent } from "../../../components/Sections/Main";

const Chatbox = () => {
  const router = useRouter();
  const { chatID, threadID } = router.query;
  const [config, setConfig] = useState({});
  const [datas, setData] = useState([]);
  const [query, setQuery] = useState();
  const [isAsk, setIsAsk] = useState(false);
  const [leadpass, setLeadpass] = useState(false);
  const intervalRef = useRef(null);
  const divEndRef = useRef(null);

  const typingEffect = async (str) => {
    let i = 0;
    const str_length = str.length;

    intervalRef.current = setInterval(() => {
      //console.log(intervalRef.current);
      if (i < str_length) {
        // Update the appropriate DOM element using React's refs
        const msgContent = document.querySelector(
          ".messages-list .bot-msg:nth-last-child(2) .msg-content"
        );
        msgContent.innerHTML = str.slice(0, i + 1);
        i++;
      } else {
        clearInterval(intervalRef.current);
        // Add your additional logic here, for example:
        // Remove classes, scroll to bottom, etc.
        document
          .querySelector(".sai-chatbox-area")
          .classList.remove("has-messages");
        document.querySelector(".sai-chatbox-area").scrollTop =
          document.querySelector(".sai-chatbox-area").scrollHeight;
      }
    }, 10);

    return () => {
      const msgContent = document.querySelector(
        ".messages-list .bot-msg:nth-last-child(2) .msg-content"
      );
      msgContent.innerHTML = "";
      clearInterval(intervalRef.current); // Clear the interval when the component unmounts
    };
  };

  const messageAction = async (message) => {
    let chat_history, newresponse, response, botLoading;
    
    botLoading = {
      message: <DotLoading />,
      type: "bot",
      chatbot_id: chatID,
      thread_id: threadID,
      date: Date.now(),
      source:''
    };
    chat_history = datas;
    const history_messages = chat_history.map((item) => {
      const { message } = item;
      return message;
    });
    const result = [];
for (let i = 0; i < history_messages.length; i += 2) {
  const chunk = history_messages.slice(i, i + 2);
  result.push(chunk);
}

    
    setData((prevData) => [...prevData, botLoading]);
    const textArea = document.getElementById("autosize-textarea");
    textArea.style.removeProperty("height");
    response = await postMessage(chatID, threadID, message, result);
    newresponse = {
      message:response.response,
        // response.success == true
        //   ? response.answer
        //   : "An error occurred, I'm unable to answer your question.",
      source:"",
      type: "bot",
      chatbot_id: chatID,
      thread_id: threadID,
      date: new Date(),
    };
    await setData((prevData) => {
      const newData = [...prevData]; // Create a copy of the previous data array
      if (newData.length > 0) {
        newData[newData.length - 1] = newresponse; // Update the last value with the desired new value
      }
      return newData; // Return the updated data array
    });
    await typingEffect(response.response);
      // await typingEffect(response.success == true
      //   ? response.answer
      //   : "An error occurred, I'm unable to answer your question.");
  };

  const sendMessage = async (message) => {
    const newMessage = {
      message: message,
      type: "user",
      chatbot_id: chatID,
      thread_id: threadID,
      date: Date.now(),
    };
    if (datas.length === 0) {
      await setData([newMessage]);
    }else{
      await setData((prevData) => [...prevData, newMessage]);
    }
    // } else if (datas[datas.length - 1].type === "bot") {
    //   await setData((prevData) => [...prevData, newMessage]);
    // } else if (datas[datas.length - 1].type === "user") {
    //   await setData((prevData) => {
    //     const newData = [...prevData];
    //     if (newData.length > 0) {
    //       newData[newData.length - 1] = newMessage;
    //     }
    //     return newData;
    //   });
    // }
    //console.log(datas)
    
    setQuery("");
    if (!leadpass) {
      if (
        config["force_lead_collecting"] === "on" &&
        config["collect_leads"] === "on"
      ) {
        setIsAsk(true);
        console.log('hereeeeeee')
        divEndRef.current.scrollIntoView({ behavior: "smooth" });
      } else if (
        config["collect_leads"] === "on" &&
        config["force_lead_collecting"] === "off"
      ) {
        setIsAsk(false);
        await messageAction(message);
        setIsAsk(true);
        divEndRef.current.scrollIntoView({ behavior: "smooth" });
      }else{
        messageAction(message);
      }
    } else {
      messageAction(message);
    }
  };

  const refreshChat = () => {
    //console.log("Refresh");
    removeData(chatID, threadID);
    setData([]);

  };

  const closeChat = () => {
    //console.log("Close");
    window.parent.postMessage({ isOpen: false }, '*');
  };

  useEffect(()=>{
    divEndRef.current.scrollIntoView({ behavior: "smooth" })
  }, [datas, isAsk]);

  useEffect(() => {
    const textArea = document.getElementById("autosize-textarea");
    textArea.addEventListener(
      "input",
      (e) => {
        autoResize(e.target);
      },
      false
    );
  }, [query]);

  useEffect(() => {
    const fetchData = async () => {
      if (chatID) {
        try {
          //console.log(chatID, threadID);
          let configuration = await getData(chatID);
          const parsedData = JSON.parse(configuration[0].configuration);
          console.log(parsedData);
          let messages = [];
          let checkLead = await leadCheck(threadID, chatID);
          //console.log('checkcheck',checkLead)
          await setConfig(parsedData);
          await setData(messages);
          await setLeadpass(checkLead);
          //console.log(document.body.scrollHeight);
          window.scrollTo(0, document.body.scrollHeight);
        } catch (error) {
          //console.error(error);
        }
      }
    };
    //console.log("loading.....", chatID);
    fetchData();
  }, [chatID, threadID]);

  return (
    <div className="sai-chatbox">
      <Header config={config} refreshChat={refreshChat} closeChat={closeChat} />
      <div className="sai-chatbox-area">
        <div className="flex flex-1 flex-col justify-end gap-2 messages-list">
          <WelcomeComponent config={config}/>
          <MainComponent config={config} datas={datas}/>
          <div className="bot-msg" ref={divEndRef}>
            {isAsk && !leadpass ? (
              <LeadComponent
                leads_title={config["leads-title"]}
                leads_field={config["lead_fields"]}
                setClose={setLeadpass}
                force={config["force_lead_collecting"]}
                thread_id={threadID}
                chat_id={chatID}
                messageAction={messageAction}
                datas={datas}
              />
            ) : (
              <></>
            )}
          </div>
        </div>
      </div>
      <Footer
        config={config}
        query={query}
        setQuery={setQuery}
        sendMessage={sendMessage}
      />
    </div>
  );
};

export default Chatbox;

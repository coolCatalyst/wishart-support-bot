import React, { useEffect, useState } from "react";
import { v4 as uuidv4 } from "uuid";
import { useRouter } from "next/router";
const Chatbox = () => {
  const router = useRouter();
  const { chatID } = router.query;

  useEffect(() => {
    if (chatID) {
      let threadId;
      threadId = localStorage.getItem('threadId');
      //console.log('first loading', threadId)
      if(threadId==null){
        threadId  = uuidv4();
        localStorage.setItem('threadId', threadId);
      }
      router.push(`/${chatID}/threads/${threadId}`);
    }
  }, [chatID]);

  return <div></div>;
};
export default Chatbox;

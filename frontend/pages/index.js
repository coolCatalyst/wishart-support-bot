import { useRouter } from 'next/router';
import { useEffect } from 'react';
import { v4 as uuidv4 } from "uuid";

const HomePage = () => {
  const router = useRouter();

  useEffect(() => {
    let chatID;
    chatID = localStorage.getItem('chatID');
    //console.log('first loading', threadId)
    if (chatID == null) {
      chatID = uuidv4();
      localStorage.setItem('chatID', chatID);
    }
    router.push(`/${chatID}`);
  }, []);

  return (
    <div>
    </div>
  );
};

export default HomePage;
import { useRouter } from 'next/router';
import { useEffect } from 'react';

const HomePage = () => {
  const router = useRouter();
  const { chatID } = router.query;
  const staticChatID = 'staticID'; 

  useEffect(() => {
    if (chatID) {
      router.push(`/${chatID}`);
    }else{
      router.push(`/${staticChatID}`);
    }
  }, [chatID, staticChatID, router]);

  return (
    <div>
    </div>
  );
};

export default HomePage;
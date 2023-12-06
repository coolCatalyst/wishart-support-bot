import { useRouter } from 'next/router';
import { useEffect } from 'react';

const HomePage = () => {
  const router = useRouter();
  const { chatID, threadID } = router.query;

  useEffect(() => {
    if (chatID) {
      router.push(`/${chatID}`);
    }
  }, [chatID, threadID]);

  return (
    <div>
      <h1>Home Page</h1>
    </div>
  );
};

export default HomePage;
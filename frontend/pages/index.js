import { useRouter } from 'next/router';
import { useEffect } from 'react';

const HomePage = () => {
  const router = useRouter();
  const { chatID } = router.query;
  const staticID = "chat"

  useEffect(() => {
    if (chatID) {
      router.push(`/${chatID}`);
    }else{
      router.push(`/${staticID}`);
    }
  }, [chatID]);

  return (
    <div>
    </div>
  );
};

export default HomePage;
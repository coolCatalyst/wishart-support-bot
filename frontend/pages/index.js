import { useRouter } from 'next/router';
import { useEffect } from 'react';

const HomePage = () => {
  const router = useRouter();
  const { chatID } = router.query;

  useEffect(() => {
    if (chatID) {
      router.push(`/${chatID}`);
    }else{
      router.push('https://supportai.com')
    }
  }, [chatID]);

  return (
    <div>
    </div>
  );
};

export default HomePage;
import logo from '../../logo.svg';
import './Topbar.css';
import { useTheme, ChakraProvider, Flex, Spacer, Box, Center, Text, theme} from '@chakra-ui/react'
import { Link } from 'react-router-dom';
import Logo from './Logo.js';
import ProfileMenu from './ProfileMenu.js';

function Topbar() {
  const theme = useTheme();
  let isLoggedIn = false;
  // if page is not / or /signup, then user is logged in
  if (window.location.pathname !== '/' && window.location.pathname !== '/signup') {
    isLoggedIn = true;
  }

  
  return (
    <Flex className="w-full h-16 fixed top-0 left-0  z-50 drop-shadow-xl" align="center" bg={theme.colors.brand.topbar}>
      <Box p="2" className="flex-grow-0">
        <Flex align="center"> {/* This ensures vertical center alignment */}
          <Logo className='h-full w-auto'/>
          {/* Ensure Text component inherits Flex alignment; removed 'items-center' as it's not a valid prop here */}
          <Text color="white" ml={2} fontFamily="Berkeley Mono" fontSize={'xl'}>Boardly</Text>
        </Flex>
      </Box>
      <Spacer />
      <Box p="2">
        {/* <Center className="h-full cursor-pointer">
          {isLoggedIn && <ProfileMenu />} 
        </Center> */}
      </Box>
    </Flex>
  );
}

export default Topbar;
/* eslint-disable react-native/no-inline-styles */
import React, {useEffect, useState} from 'react';
import {View, Text} from 'react-native';
import LoadingActionContainer from '../../Components/LoadingActionContainer';
import {Container, HeaderButton, InputX} from '../../Components';
import useAppTheme from '../../Themes/Context';
import {IconX, ICON_TYPE} from '../../Icons';
import {useStoreState} from 'easy-peasy';
import Fonts from '../../Themes/Fonts';
import {TouchableOpacity, ListItem} from 'react-native';
import {ButtonX} from '../../Components';
import AudioRecord from 'react-native-audio-record';
import Tts from 'react-native-tts';
import {BASE_URL} from '../../Config/index';
import AsyncStorage from '@react-native-community/async-storage';

const MainScreen = ({routes, route, navigation}) => {
  const {theme} = useAppTheme();
  // eslint-disable-next-line prettier/prettier
  const {username, password} = useStoreState((state) => ({
    username: state.login.username,
    password: state.login.password,
  }));
  const {response} = route.params;

  useEffect(() => {
    console.log('💒', response);
    const _toggleDrawer = () => {
      navigation.toggleDrawer();
    };
    const options = {
      sampleRate: 16000, // default 44100
      channels: 1, // 1 or 2, default 1
      bitsPerSample: 16, // 8 or 16, default 16
      audioSource: 6, // android only (see below)
      wavFile: 'test.wav', // default 'audio.wav'
    };

    AudioRecord.init(options);
    Tts.speak(response.msg, {
      androidParams: {
        KEY_PARAM_PAN: -1,
        KEY_PARAM_VOLUME: 0.5,
        KEY_PARAM_STREAM: 'STREAM_MUSIC',
      },
    });
    Tts.speak(`payment${response.payment}`, {
      androidParams: {
        KEY_PARAM_PAN: -1,
        KEY_PARAM_VOLUME: 0.5,
        KEY_PARAM_STREAM: 'STREAM_MUSIC',
      },
    });
    Tts.speak(`total${response.total}$`, {
      androidParams: {
        KEY_PARAM_PAN: -1,
        KEY_PARAM_VOLUME: 0.5,
        KEY_PARAM_STREAM: 'STREAM_MUSIC',
      },
    });
    console.log('use effect home');
  }, [navigation, theme.colors.headerTitle]);
  const names = ['Bruce', 'Clark', 'Diana'];

  const record = () => {
    // console.log('record');

    // AudioRecord.start();
    // timeout;
    // let timeout = setTimeout(() => {
    //   stopRecord();
    //   console.log('hello');
    // }, 5000);
  };

  const stopRecord = async () => {
    // console.log('recordStop ');
    // const audioFile = await AudioRecord.stop();
    // AudioRecord.on('data', (data) => {});
    // console.log('audioFile 🍷', audioFile);
    // initialRec(audioFile);
    // AudioRecord.stop();
  };
  const initialRec = (audioFile) => {
    uploadAudio(audioFile);
    console.log('initialRec', audioFile);
    const options = {
      sampleRate: 16000, // default 44100
      channels: 1, // 1 or 2, default 1
      bitsPerSample: 16, // 8 or 16, default 16
      audioSource: 6, // android only (see below)
      wavFile: 'test.wav', // default 'audio.wav'
    };
  };
  const uploadAudio = async (fileUrl) => {
    // console.log('upload');
    // console.log('🧑‍🚀🧑‍🚀', fileUrl);
    // let formData = new FormData();
    // formData.append('audioFile', {
    //   uri: 'file:///data/user/0/com.easy_boiler/files/test.wav',
    //   type: 'audio/wav',
    //   name: 'test.wav',
    // });
    // formData.append('flag', 'name');
    // formData.append('userId', 3);
    // console.log(formData);

    // fetch(`${BASE_URL}/voicesearch/en`, {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'multipart/form-data',
    //   },
    //   body: formData,
    // })
    //   .then((response) => response.json())
    //   .then((response) => {
    //     console.log('response 🔥', response.flag);
    //     console.log(response);
    //     if (response.flag == 'back') {
    //       navigation.navigate('language-success');
    //     }
    //     if (response.flag == 'place-order') {
    //       navigation.navigate('place-order', {
    //         response,
    //       });
    //     }
    //     if (response.flag == 'search-save') {
    //       navigation.navigate('search-save', {
    //         response,
    //       });
    //     }
    //     if (response.flag == 'checkout') {
    //       Tts.speak(response.msg, {
    //         androidParams: {
    //           KEY_PARAM_PAN: -1,
    //           KEY_PARAM_VOLUME: 0.5,
    //           KEY_PARAM_STREAM: 'STREAM_MUSIC',
    //         },
    //       });
    //       navigation.navigate('language-success');
    //     }
    //     if (response.flag == 'check-order') {
    //       navigation.navigate('check-order');
    //     } else {
    //       console.log('route error');
    //     }
    //   })
    //   .catch((err) => console.error(err));
  };

  return (
    <LoadingActionContainer fixed>
      <Container
        style={{
          padding: 10,
        }}>
        <View
          style={{
            flex: 1,
            flexDirection: 'column',
            justifyContent: 'space-around',
          }}>
          <View
            style={{
              flex: 1,
              flexDirection: 'row',
              justifyContent: 'space-around',
            }}>
            <View style={{alignItems: 'center'}}>
              <TouchableOpacity>
                <View
                  style={{
                    padding: 10,
                    marginTop: 20,
                    backgroundColor: theme.colors.primary,
                    borderRadius: 10,
                  }}>
                  <Text
                    style={{
                      color: '#fff',
                      fontSize: 14,
                      textAlign: 'left',
                      padding: 5,
                    }}>
                    Address:
                  </Text>
                  <Text
                    style={{
                      color: '#fff',
                      fontSize: 14,
                      textAlign: 'left',
                      padding: 5,
                    }}>
                    {response.address}
                    {/* 40074-6659,{'\n'}Lake Paula,{'\n'}Colombia */}
                  </Text>
                </View>
              </TouchableOpacity>
            </View>
            <View style={{alignItems: 'center'}}>
              <TouchableOpacity onPress={record}>
                <View
                  style={{
                    padding: 10,
                    marginTop: 20,
                    backgroundColor: theme.colors.primary,
                    borderRadius: 10,
                  }}>
                  <IconX name={'md-mic'} style={{color: '#fff'}} />
                </View>
              </TouchableOpacity>
            </View>
          </View>
          <View
            style={{
              flex: 1,
              flexDirection: 'row',
              justifyContent: 'space-around',
            }}>
            <View style={{alignItems: 'center'}}>
              <TouchableOpacity>
                <View>
                  <Text
                    style={{
                      color: '#111',
                      fontSize: 14,
                      textAlign: 'left',
                      padding: 5,
                    }}>
                    Total Amount:
                  </Text>
                </View>
              </TouchableOpacity>
            </View>
            <View style={{alignItems: 'center'}}>
              <TouchableOpacity>
                <View>
                  <Text
                    accessible={true}
                    accessibilityLabel={`Your Total is `+response.total}
                    accessibilityRole="text"
                    style={{
                      color: '#111',
                      fontSize: 14,
                      textAlign: 'left',
                      padding: 5,
                    }}>
                    {response.total}$
                  </Text>
                </View>
              </TouchableOpacity>
            </View>
          </View>
          <ButtonX
            accessible={true} 
            accessibilityLabel="Read Order" 
            accessibilityHint="Read your Order"
            accessibilityRole="button"
            dark={true}
            color={theme.colors.primary}
            onPress={() => navigation.navigate('ProductList')}
            label={'Read'}
          />
          <ButtonX
            accessible={true} 
            accessibilityLabel="Edit Order" 
            accessibilityHint="Edit your Order"
            accessibilityRole="button"
            dark={true}
            color={theme.colors.primary}
            onPress={() => navigation.navigate('ProductList')}
            label={'Edit'}
          />
          <ButtonX
            accessible={true} 
            accessibilityLabel="Place Order" 
            accessibilityHint="Place your Order"
            accessibilityRole="button"
            dark={true}
            color={theme.colors.primary}
            onPress={() => navigation.navigate('ProductList')}
            label={'Place Order'}
          />
        </View>
      </Container>
    </LoadingActionContainer>
  );
};

export default MainScreen;

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
import {RNCamera} from 'react-native-camera';
import axios from 'axios';
import AudioRecord from 'react-native-audio-record';
import {BASE_URL} from '../../Config/index';
import AsyncStorage from '@react-native-community/async-storage';
import Spinner from 'react-native-loading-spinner-overlay';
import * as ImagePicker from 'react-native-image-picker';
const MainScreen = ({routes, navigation}) => {
  const {theme} = useAppTheme();
  // eslint-disable-next-line prettier/prettier
  const {username, password} = useStoreState((state) => ({
    username: state.login.username,
    password: state.login.password,
  }));

  useEffect(() => {
    const _toggleDrawer = () => {
      navigation.toggleDrawer();
    };

    console.log('use effect home');
  }, [navigation, theme.colors.headerTitle]);
  const names = ['Bruce', 'Clark', 'Diana'];
  let camera;
  const [spinner, setSpinner] = useState(false);
  const launchImageLibrary = () => {
    let options = {
      storageOptions: {
        skipBackup: true,
        path: 'images',
      },
    };
    ImagePicker.launchImageLibrary(options, (response) => {
      console.log('Response = ', response.assets[0].uri);
      setSpinner(true);
      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else if (response.customButton) {
        console.log('User tapped custom button: ', response.customButton);
        alert(response.customButton);
      } else {
        let formData = new FormData();
        formData.append('listFile', {
          uri: response.assets[0].uri,
          type: 'image/jpg',
          name: 'image.jpg',
        });
        fetch(`${BASE_URL}/predict`, {
          method: 'POST',
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          body: formData,
        })
          .then((response) => response.json())
          .then((response) => {
            console.log('response 🔥', response.flag);
            console.log(response);
            setSpinner(false);
            storeData(response);
          })
          .catch((err) => console.error(err));
      }
    });
  };
  async function takePicture() {
    setSpinner(true);
    if (camera) {
      const options = {
        quality: 0.5,
        base64: true,
        // orientation: 'landscape',
        // forceUpOrientation: true,
        // fixOrientation: true,
      };
      const data = await camera.takePictureAsync(options);
      const baseImage = data.base64;
      console.log('hello camera');
      let formData = new FormData();

      formData.append('listFile', {
        uri: data.uri,
        type: 'image/jpg',
        name: 'image.jpg',
      });
      fetch(`${BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        body: formData,
      })
        .then((response) => response.json())
        .then((response) => {
          console.log('response 🔥', response.flag);
          console.log(response);

          setSpinner(false);

          storeData(response);
        })
        .catch((err) => console.error(err));
    }
  }
  const storeData = async (value) => {
    try {
      const jsonValue = JSON.stringify(value);
      await AsyncStorage.setItem('@image_search', jsonValue);
      console.log(jsonValue);
      navigation.navigate('ImageSearchResultNew');
    } catch (e) {}
  };
  return (
    <LoadingActionContainer fixed>
      <Container
        style={{
          padding: 10,
        }}>
        <Spinner visible={spinner} textContent={'Loading...'} />

        <View
          style={{
            flex: 1,
            flexDirection: 'column',
            justifyContent: 'space-around',
          }}>
          <View style={{flex: 1, width: '100%'}}>
            <RNCamera
              ref={(ref) => (camera = ref)}
              style={{flex: 1}}
              type={RNCamera.Constants.Type.back}
              flashMode={RNCamera.Constants.FlashMode.off}
              androidCameraPermissionOptions={{
                title: 'Permission to use camera',
                message: 'We need your permission to use your camera',
                buttonPositive: 'Ok',
                buttonNegative: 'Cancel',
              }}
              androidRecordAudioPermissionOptions={{
                title: 'Permission to use audio recording',
                message: 'We need your permission to use your audio',
                buttonPositive: 'Ok',
                buttonNegative: 'Cancel',
              }}
            />
          </View>
          <ButtonX
            accessible={true}
            accessibilityLabel="Save Changes"
            accessibilityHint="Save Changes made to your Grocery List"
            accessibilityRole="button"
            dark={true}
            color={theme.colors.primary}
            onPress={() => navigation.navigate('ImageSearchResultNew')}
            label={'Save Changes'}
          />
          <ButtonX
            accessible={true}
            accessibilityLabel="Capture Picture"
            accessibilityHint="Take Image of Grocery List from Camera"
            accessibilityRole="button"
            dark={true}
            color={theme.colors.primary}
            onPress={() => takePicture()}
            label={'Capture'}
          />
          <ButtonX
            accessible={true}
            accessibilityLabel="Load from Gallery"
            accessibilityHint="Load Image of Grocery List from Gallery"
            accessibilityRole="button"
            dark={true}
            color={theme.colors.primary}
            onPress={() => launchImageLibrary()}
            label={'Upload'}
          />
        </View>
      </Container>
    </LoadingActionContainer>
  );
};

export default MainScreen;

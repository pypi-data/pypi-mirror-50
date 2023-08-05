export enum DeviceTypeEnum {
    MOBILE_WEB,
    MOBILE_IOS,
    MOBILE_ANDROID,
    DESKTOP_WEB,
    DESKTOP_WINDOWS,
    DESKTOP_MACOS
}


export abstract class HardwareInfoI {
    abstract uuid(): Promise<string> ;

    abstract description(): string;

    abstract deviceType(): DeviceTypeEnum;

    isWeb(): boolean {
        return this.deviceType() == DeviceTypeEnum.MOBILE_WEB
            || this.deviceType() == DeviceTypeEnum.DESKTOP_WEB;
    }
}

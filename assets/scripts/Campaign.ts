export const CHAPTERS=[
 {title:'Những bữa picnic đầu',theme:'Làm quen, Cơm cùng Rau, Kem xa Súp'},
 {title:'Những lời nhờ nhỏ',theme:'Dâu sát viền và phối hợp sở thích'},
 {title:'Chỗ hẹn trong hộp',theme:'Phủ đúng món lên ô được đánh dấu'},
 {title:'Dải ruy băng nhỏ',theme:'Món có khóa được di chuyển, không được xoay'},
 {title:'Chiếc bánh được che',theme:'Toàn bộ Bánh nằm bên trong hộp'},
 {title:'Hai ngăn, một bữa',theme:'Chọn ngăn, vượt góc hẹp, chia khoảng trống'},
 {title:'Những lời hứa chung',theme:'Phối hợp các điều bạn bè yêu thích'},
 {title:'Hộp quà khéo léo',theme:'Hướng cố định và những khoảng trống khó'},
 {title:'Picnic bậc thầy',theme:'Tổng hợp, thử thách và những bữa nghỉ'}
];
export const RULE_SHORT:Record<string,string>={rice:'Cơm chạm Rau',cold:'Kem xa Súp',edge:'Dâu sát viền',target:'Phủ đúng ô món',fixed:'Khóa = không xoay',center:'Bánh không chạm viền'};
export const RULE_HELP:Record<string,string>={
 rice:'Cơm cần chạm cạnh Rau. Chạm chéo không tính.',
 cold:'Kem không được chạm cạnh Súp.',
 edge:'Ít nhất một ô Dâu chạm viền ngoài hộp.',
 target:'Ô có hình món và ngôi sao là chỗ hẹn.\nĐặt đúng loại món phủ lên ô đó.\nChạm ô đánh dấu để xem món cần đặt.',
 fixed:'Món có khóa giữ nguyên hướng trong khay.\nBạn vẫn có thể di chuyển, bỏ ra và hoàn tác.\nHãy xoay các món khác để nhường chỗ.',
 center:'Toàn bộ miếng Bánh phải ở bên trong hộp.\nKhông ô Bánh nào được chạm viền ngoài.\nCác món khác vẫn có thể nằm sát viền.'
};

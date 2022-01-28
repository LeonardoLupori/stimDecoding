function saveRawData(m, data, trial, repNumber)

switch trial
    case 'triangle'
        m.rawTriangle(:,:,:,repNumber) = data;
    case 'cross'
        m.rawCross(:,:,:,repNumber) = data;
    case 'circle'
        m.rawCircle(:,:,:,repNumber) = data;
    case 'square'
        m.rawSquare(:,:,:,repNumber) = data;
    case 'h_letter'
        m.rawLetter_H(:,:,:,repNumber) = data;
    case 'v_letter'
        m.rawLetter_V(:,:,:,repNumber) = data;
    case 'star'
        m.rawStar(:,:,:,repNumber) = data;
    case 't_letter'
        m.rawLetter_T(:,:,:,repNumber) = data;
    case 's_letter'
        m.rawLetter_S(:,:,:,repNumber) = data;
    case 'w_letter'
        m.rawLetter_W(:,:,:,repNumber) = data;
end

